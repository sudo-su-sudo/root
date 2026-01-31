"""
Web Interface for Learning Orchestrator

A Flask-based web application that provides a mobile-friendly interface
for interacting with the Learning Orchestrator.
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import secrets
from datetime import datetime
from orchestrator import LearningOrchestrator, Boundary, BoundaryType

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Store orchestrator instances per session
orchestrators = {}


def get_orchestrator():
    """Get or create orchestrator for current session"""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(8)
    
    session_id = session['session_id']
    
    if session_id not in orchestrators:
        orch = LearningOrchestrator()
        # Set some default framework
        orch.update_user_framework(
            goals=["Learn and grow", "Make good decisions"],
            values=["Quality", "Efficiency", "Security"],
            intent="Explore and learn preferences"
        )
        orchestrators[session_id] = orch
    
    return orchestrators[session_id]


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current learning status"""
    orch = get_orchestrator()
    summary = orch.get_learning_summary()
    progress = orch.get_progress_update()
    
    can_act, reason = orch.should_act_autonomously()
    
    return jsonify({
        'understanding_level': summary['understanding_level'],
        'decision_count': summary['decision_history_size'],
        'patterns_identified': summary['identified_patterns'],
        'can_act_autonomously': can_act,
        'autonomous_reason': reason,
        'progress_summary': progress.summary,
        'alignment_check': progress.alignment_check,
        'key_insights': progress.key_insights,
        'next_steps': progress.next_steps,
        'dimension_scores': summary['dimension_scores'],
        'strong_patterns': summary.get('strong_patterns', []),
        'confident_hypotheses': summary.get('confident_hypotheses', [])
    })


@app.route('/api/record_decision', methods=['POST'])
def record_decision():
    """Record a user decision"""
    data = request.json
    orch = get_orchestrator()
    
    try:
        orch.record_user_decision(
            situation=data['situation'],
            chosen_option=data['chosen'],
            rejected_options=data.get('rejected', []),
            reasoning=data.get('reasoning', ''),
            constraints=data.get('constraints', {})
        )
        
        # Get updated status
        summary = orch.get_learning_summary()
        
        return jsonify({
            'success': True,
            'message': 'Decision recorded! I learned from your choice.',
            'understanding_level': summary['understanding_level'],
            'new_insights': orch.insights[-3:] if orch.insights else []
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/predict', methods=['POST'])
def predict_decision():
    """Get prediction for a decision"""
    data = request.json
    orch = get_orchestrator()
    
    try:
        situation = data['situation']
        options = data['options']
        
        chosen, confidence, reasoning, needs_confirm = orch.make_autonomous_decision(
            situation, options, require_high_confidence=False
        )
        
        return jsonify({
            'success': True,
            'chosen': chosen,
            'confidence': int(confidence * 100),
            'reasoning': reasoning,
            'needs_confirmation': needs_confirm,
            'all_options': options
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/explain_uncertainty', methods=['POST'])
def explain_uncertainty():
    """Get explanation of uncertainty for a decision"""
    data = request.json
    orch = get_orchestrator()
    
    try:
        context = data['context']
        explanation = orch.explain_uncertainty(context)
        
        # Also get critical gaps
        gaps = orch.identify_critical_gaps(context)
        
        gap_details = []
        for gap in gaps[:3]:  # Top 3
            gap_details.append({
                'area': gap.area,
                'description': gap.description,
                'root_cause': gap.root_cause.value,
                'impact': gap.impact_on_decision,
                'resolution': gap.suggested_resolution
            })
        
        return jsonify({
            'success': True,
            'explanation': explanation,
            'gaps': gap_details
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/framework', methods=['GET', 'POST'])
def manage_framework():
    """Get or update user framework"""
    orch = get_orchestrator()
    
    if request.method == 'GET':
        return jsonify({
            'goals': orch.user_framework.goals,
            'values': orch.user_framework.values,
            'intent': orch.user_framework.intent,
            'context': orch.user_framework.context
        })
    
    else:  # POST
        data = request.json
        try:
            orch.update_user_framework(
                goals=data.get('goals'),
                values=data.get('values'),
                intent=data.get('intent'),
                context=data.get('context')
            )
            return jsonify({
                'success': True,
                'message': 'Framework updated successfully'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400


@app.route('/api/boundaries', methods=['GET', 'POST'])
def manage_boundaries():
    """Get or add boundaries"""
    orch = get_orchestrator()
    
    if request.method == 'GET':
        boundaries = []
        for b in orch.boundaries:
            boundaries.append({
                'type': b.type,
                'description': b.description,
                'value': b.value,
                'category': b.category
            })
        return jsonify({'boundaries': boundaries})
    
    else:  # POST
        data = request.json
        try:
            boundary = Boundary(
                type=BoundaryType(data['type']),
                description=data['description'],
                value=data['value'],
                category=data.get('category')
            )
            orch.add_boundary(boundary)
            return jsonify({
                'success': True,
                'message': 'Boundary added successfully'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400


@app.route('/api/reset', methods=['POST'])
def reset_session():
    """Reset the current session"""
    if 'session_id' in session:
        session_id = session['session_id']
        if session_id in orchestrators:
            del orchestrators[session_id]
        session.clear()
    
    return jsonify({
        'success': True,
        'message': 'Session reset successfully'
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat interface - natural language interaction"""
    data = request.json
    message = data.get('message', '').lower()
    orch = get_orchestrator()
    
    # Simple command parsing
    if 'status' in message or 'how am i doing' in message or 'progress' in message:
        progress = orch.get_progress_update()
        return jsonify({
            'response': f"📊 {progress.summary}\n\n🎯 {progress.alignment_check}",
            'type': 'status'
        })
    
    elif 'help' in message or 'what can you do' in message:
        return jsonify({
            'response': """I'm your Learning Orchestrator! Here's what I can do:

📝 **Record Decisions** - Tell me about choices you make and why
🔮 **Make Predictions** - I'll predict what you'd choose based on what I've learned
🧠 **Explain Gaps** - I'll tell you exactly what I don't know and why
📊 **Show Progress** - Track how well I understand your preferences
🎯 **Meta-Reasoning** - Identify root causes of uncertainty

Try saying:
• "Show me my progress"
• "I made a decision"
• "Help me decide"
• "What don't you know about me?"
""",
            'type': 'help'
        })
    
    elif 'decide' in message or 'predict' in message or 'choose' in message:
        return jsonify({
            'response': "I can help you decide! Please tell me:\n1. What's the situation?\n2. What are your options?",
            'type': 'prompt',
            'action': 'predict'
        })
    
    elif 'decision' in message or 'i chose' in message or 'i picked' in message:
        return jsonify({
            'response': "Great! Tell me about your decision:\n1. What was the situation?\n2. What did you choose?\n3. What did you reject?\n4. Why did you choose it?",
            'type': 'prompt',
            'action': 'record'
        })
    
    elif 'gap' in message or 'uncertain' in message or "don't know" in message:
        return jsonify({
            'response': "I can explain what I'm uncertain about. What context or decision area should I analyze?",
            'type': 'prompt',
            'action': 'explain'
        })
    
    else:
        # Default response
        summary = orch.get_learning_summary()
        return jsonify({
            'response': f"I'm learning about you! So far I understand your preferences at {summary['understanding_level']}.\n\nAsk me for 'help' to see what I can do!",
            'type': 'info'
        })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Learning Orchestrator Web Interface Starting...")
    print("="*60)
    print("\n📱 Open in your browser: http://localhost:5000")
    print("🌐 Mobile-friendly interface ready!")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
