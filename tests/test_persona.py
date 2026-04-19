"""
Tests for Persona System
"""

import pytest
import json
import os
from datetime import datetime

from orchestrator import (
    Persona,
    PersonaCore,
    PersonaBehavior,
    PersonaKnowledge,
    PersonaType,
    SummoningProtocol,
    PersonaPersistence,
    create_epiphany_architect
)


class TestPersonaCore:
    """Test PersonaCore functionality"""
    
    def test_create_core(self):
        """Test creating a persona core"""
        core = PersonaCore(
            name="Test Persona",
            persona_type=PersonaType.ARCHITECT,
            description="A test persona"
        )
        
        assert core.name == "Test Persona"
        assert core.persona_type == PersonaType.ARCHITECT
        assert core.description == "A test persona"
        assert core.version == "1.0.0"
        assert core.created_at is not None
    
    def test_core_timestamp(self):
        """Test that created_at timestamp is set"""
        core = PersonaCore(
            name="Test",
            persona_type=PersonaType.ANALYST,
            description="Test"
        )
        
        # Should be parseable as datetime
        dt = datetime.fromisoformat(core.created_at)
        assert isinstance(dt, datetime)


class TestPersonaBehavior:
    """Test PersonaBehavior functionality"""
    
    def test_create_behavior(self):
        """Test creating persona behavior"""
        behavior = PersonaBehavior(
            operating_principles=["Principle 1", "Principle 2"],
            core_methods=["Method 1", "Method 2"],
            tone_descriptors=["Warm", "Precise"],
            interaction_style="Professional",
            primary_goal="Test goal"
        )
        
        assert len(behavior.operating_principles) == 2
        assert len(behavior.core_methods) == 2
        assert len(behavior.tone_descriptors) == 2
        assert behavior.interaction_style == "Professional"
        assert behavior.primary_goal == "Test goal"
    
    def test_to_dict(self):
        """Test behavior serialization"""
        behavior = PersonaBehavior(
            operating_principles=["P1"],
            core_methods=["M1"],
            tone_descriptors=["T1"],
            interaction_style="Style",
            primary_goal="Goal"
        )
        
        data = behavior.to_dict()
        assert isinstance(data, dict)
        assert data['operating_principles'] == ["P1"]
        assert data['primary_goal'] == "Goal"


class TestPersonaKnowledge:
    """Test PersonaKnowledge functionality"""
    
    def test_create_knowledge(self):
        """Test creating persona knowledge"""
        knowledge = PersonaKnowledge(
            expertise_areas=["Area 1", "Area 2"],
            capabilities=["Cap 1", "Cap 2"],
            constraints=["Con 1"],
            metadata={"key": "value"}
        )
        
        assert len(knowledge.expertise_areas) == 2
        assert len(knowledge.capabilities) == 2
        assert len(knowledge.constraints) == 1
        assert knowledge.metadata["key"] == "value"


class TestPersona:
    """Test Persona functionality"""
    
    def create_test_persona(self):
        """Helper to create a test persona"""
        core = PersonaCore(
            name="Test Persona",
            persona_type=PersonaType.ARCHITECT,
            description="Test"
        )
        
        behavior = PersonaBehavior(
            operating_principles=["P1"],
            core_methods=["M1"],
            tone_descriptors=["T1"],
            interaction_style="Style",
            primary_goal="Goal"
        )
        
        knowledge = PersonaKnowledge(
            expertise_areas=["Area"],
            capabilities=["Cap"],
            constraints=["Con"],
            metadata={}
        )
        
        return Persona(core, behavior, knowledge)
    
    def test_create_persona(self):
        """Test creating a persona"""
        persona = self.create_test_persona()
        
        assert persona.core.name == "Test Persona"
        assert persona.conversation_count == 0
        assert isinstance(persona.state, dict)
    
    def test_update_state(self):
        """Test updating persona state"""
        persona = self.create_test_persona()
        
        persona.update_state("key1", "value1")
        persona.update_state("key2", 123)
        
        assert persona.state["key1"] == "value1"
        assert persona.state["key2"] == 123
    
    def test_increment_conversation(self):
        """Test conversation tracking"""
        persona = self.create_test_persona()
        
        assert persona.conversation_count == 0
        
        persona.increment_conversation()
        assert persona.conversation_count == 1
        
        persona.increment_conversation()
        assert persona.conversation_count == 2
    
    def test_to_dict(self):
        """Test persona serialization"""
        persona = self.create_test_persona()
        persona.update_state("test_key", "test_value")
        
        data = persona.to_dict()
        
        assert isinstance(data, dict)
        assert 'core' in data
        assert 'behavior' in data
        assert 'knowledge' in data
        assert 'state' in data
        assert data['state']['test_key'] == "test_value"
    
    def test_to_json(self):
        """Test JSON serialization"""
        persona = self.create_test_persona()
        
        json_str = persona.to_json()
        data = json.loads(json_str)
        
        assert data['core']['name'] == "Test Persona"
        assert data['core']['persona_type'] == "architect"
    
    def test_from_json(self):
        """Test JSON deserialization"""
        persona = self.create_test_persona()
        json_str = persona.to_json()
        
        restored = Persona.from_json(json_str)
        
        assert restored.core.name == persona.core.name
        assert restored.core.persona_type == persona.core.persona_type
        assert restored.behavior.primary_goal == persona.behavior.primary_goal


class TestSummoningProtocol:
    """Test SummoningProtocol functionality"""
    
    def create_test_components(self):
        """Helper to create test components"""
        core = PersonaCore(
            name="Test Persona",
            persona_type=PersonaType.ARCHITECT,
            description="Test"
        )
        
        behavior = PersonaBehavior(
            operating_principles=["P1", "P2"],
            core_methods=["M1"],
            tone_descriptors=["T1", "T2"],
            interaction_style="Style",
            primary_goal="Goal"
        )
        
        knowledge = PersonaKnowledge(
            expertise_areas=["Area"],
            capabilities=["Cap"],
            constraints=["Con"],
            metadata={}
        )
        
        return core, behavior, knowledge
    
    def test_create_protocol(self):
        """Test creating a summoning protocol"""
        core, behavior, knowledge = self.create_test_components()
        
        protocol = SummoningProtocol.create_protocol(
            core, behavior, knowledge
        )
        
        assert "Test Persona" in protocol
        assert "SUMMONING PROTOCOL" in protocol
        assert "OPERATING PRINCIPLES" in protocol
        assert "P1" in protocol
        assert "P2" in protocol
        assert "Goal" in protocol
    
    def test_create_protocol_with_state(self):
        """Test creating protocol with state"""
        core, behavior, knowledge = self.create_test_components()
        
        protocol = SummoningProtocol.create_protocol(
            core, behavior, knowledge,
            current_state="session_id: 123\ncount: 5"
        )
        
        assert "CURRENT STATE" in protocol
        assert "session_id: 123" in protocol
    
    def test_create_compact_protocol(self):
        """Test creating compact protocol"""
        core, behavior, knowledge = self.create_test_components()
        
        compact = SummoningProtocol.create_compact_protocol(
            core, behavior
        )
        
        assert "[SUMMON: Test Persona]" in compact
        assert "Type=architect" in compact
        assert "Goal=Goal" in compact


class TestEpiphanyArchitect:
    """Test The Epiphany Architect persona"""
    
    def test_create_epiphany_architect(self):
        """Test creating The Epiphany Architect"""
        architect = create_epiphany_architect()
        
        assert architect.core.name == "The Epiphany Architect"
        assert architect.core.persona_type == PersonaType.ARCHITECT
        assert len(architect.behavior.operating_principles) == 5
        assert "First-Principles Solvent" in architect.behavior.operating_principles[-1]
    
    def test_epiphany_architect_protocol(self):
        """Test generating Epiphany Architect protocol"""
        architect = create_epiphany_architect()
        
        protocol = architect.generate_summoning_protocol()
        
        assert "The Epiphany Architect" in protocol
        assert "Anti-Convention" in protocol
        assert "Recursive Meta-Cognition" in protocol
        assert "Protocol of Wonder" in protocol
        assert "First-Principles Solvent" in protocol


class TestPersonaPersistence:
    """Test PersonaPersistence functionality"""
    
    @pytest.fixture
    def db_path(self, tmp_path):
        """Create temporary database path"""
        return str(tmp_path / "test_personas.db")
    
    @pytest.fixture
    def persistence(self, db_path):
        """Create PersonaPersistence instance"""
        return PersonaPersistence(db_path)
    
    @pytest.fixture
    def test_persona(self):
        """Create a test persona"""
        core = PersonaCore(
            name="Test Persona",
            persona_type=PersonaType.ANALYST,
            description="Test"
        )
        
        behavior = PersonaBehavior(
            operating_principles=["P1"],
            core_methods=["M1"],
            tone_descriptors=["T1"],
            interaction_style="Style",
            primary_goal="Goal"
        )
        
        knowledge = PersonaKnowledge(
            expertise_areas=["Area"],
            capabilities=["Cap"],
            constraints=[],
            metadata={}
        )
        
        return Persona(core, behavior, knowledge)
    
    def test_save_persona(self, persistence, test_persona):
        """Test saving a persona"""
        persona_id = persistence.save_persona(test_persona, "test_persona")
        
        assert persona_id == "test_persona"
    
    def test_load_persona(self, persistence, test_persona):
        """Test loading a persona"""
        # Save first
        persistence.save_persona(test_persona, "test_persona")
        
        # Load
        loaded = persistence.load_persona("test_persona")
        
        assert loaded is not None
        assert loaded.core.name == test_persona.core.name
        assert loaded.core.persona_type == test_persona.core.persona_type
    
    def test_load_nonexistent_persona(self, persistence):
        """Test loading a persona that doesn't exist"""
        loaded = persistence.load_persona("nonexistent")
        
        assert loaded is None
    
    def test_save_summoning_protocol(self, persistence, test_persona):
        """Test saving summoning protocols"""
        persona_id = persistence.save_persona(test_persona, "test_persona")
        persistence.save_summoning_protocol(persona_id, test_persona)
        
        # Should not raise an error
        protocol = persistence.get_summoning_protocol(persona_id)
        assert protocol is not None
        assert "Test Persona" in protocol
    
    def test_get_summoning_protocol(self, persistence, test_persona):
        """Test retrieving summoning protocol"""
        persona_id = persistence.save_persona(test_persona, "test_persona")
        persistence.save_summoning_protocol(persona_id, test_persona)
        
        # Get full protocol
        full = persistence.get_summoning_protocol(persona_id, compact=False)
        assert "SUMMONING PROTOCOL" in full
        
        # Get compact protocol
        compact = persistence.get_summoning_protocol(persona_id, compact=True)
        assert "[SUMMON:" in compact
    
    def test_list_personas(self, persistence, test_persona):
        """Test listing personas"""
        persistence.save_persona(test_persona, "test_persona")
        
        personas = persistence.list_personas()
        
        assert len(personas) == 1
        assert personas[0]['persona_id'] == "test_persona"
        assert personas[0]['name'] == "Test Persona"
    
    def test_delete_persona(self, persistence, test_persona):
        """Test deleting a persona"""
        persistence.save_persona(test_persona, "test_persona")
        
        # Verify it exists
        loaded = persistence.load_persona("test_persona")
        assert loaded is not None
        
        # Delete
        result = persistence.delete_persona("test_persona")
        assert result is True
        
        # Verify it's gone
        loaded = persistence.load_persona("test_persona")
        assert loaded is None
    
    def test_update_persona_activity(self, persistence, test_persona):
        """Test updating persona activity"""
        persistence.save_persona(test_persona, "test_persona")
        persistence.update_persona_activity("test_persona")
        
        # Should not raise an error
        loaded = persistence.load_persona("test_persona")
        assert loaded is not None
    
    def test_export_persona(self, persistence, test_persona):
        """Test exporting persona"""
        persona_id = persistence.save_persona(test_persona, "test_persona")
        persistence.save_summoning_protocol(persona_id, test_persona)
        
        export = persistence.export_persona(persona_id, include_history=True)
        
        assert export is not None
        assert 'persona_id' in export
        assert 'persona_data' in export
        assert 'summoning_protocol' in export
        assert 'compact_protocol' in export
    
    def test_persona_state_snapshot(self, persistence, test_persona):
        """Test saving state snapshots"""
        persona_id = persistence.save_persona(test_persona, "test_persona")
        
        # Save state snapshots
        persistence.save_state_snapshot(persona_id, {"key1": "value1"})
        persistence.save_state_snapshot(persona_id, {"key2": "value2"})
        
        # Export and check history
        export = persistence.export_persona(persona_id, include_history=True)
        
        assert 'state_history' in export
        assert len(export['state_history']) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
