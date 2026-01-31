# Data Persistence Guide

## Your Data is Safe! 💾

Good news! The Learning Orchestrator now **automatically saves your data** to a database. This means:

### ✅ What This Means For You

1. **Close Browser Anytime** 
   - Your learning data persists even if you close the browser
   - All decisions and patterns are saved automatically
   - No need to worry about losing progress

2. **Phone in Pocket = Still Learning**
   - The orchestrator keeps running on the server
   - Your data is safely stored in the database
   - When you come back, everything is exactly as you left it

3. **Phone Restarts Don't Matter**
   - Data is stored on the server, not your phone
   - Restart your device, no problem!
   - Your learning history is preserved

4. **Multi-Session Support**
   - Each browser gets a unique user ID
   - Your data is tied to that ID
   - Switch devices? Just reconnect with the same ID

## How It Works

### Automatic Saving

Every time you:
- Record a decision
- Update your framework
- Add boundaries

The system **automatically saves** to the database!

### What Gets Saved

- ✅ All decisions you record
- ✅ Learned patterns and preferences
- ✅ Reasoning models
- ✅ Your framework (goals, values, intent)
- ✅ Boundaries you set
- ✅ Confidence scores
- ✅ Knowledge gaps identified

### Database Location

Your data is stored in:
```
orchestrator_data.db
```

This is a SQLite database file on the server.

## Visual Indicators

On the web interface, you'll see:

**💾 Data persisted - safe to close browser!**

Plus a timestamp showing when data was last saved:
- "saved just now"
- "saved 5m ago"
- "saved 2h ago"

## Advanced Features

### Export Your Data

```
GET /api/export
```

Downloads all your data as JSON:
- Decision history
- Framework settings
- Timestamps
- Perfect for backup!

### Manual Save

```
POST /api/save
```

Force an immediate save to database (though it auto-saves anyway).

### View Statistics

```
GET /api/stats
```

See:
- When you first started
- Last accessed time
- Last saved time
- Number of decisions
- Number of patterns

## Technical Details

### Database Schema

**user_sessions** - User accounts
- user_id (unique ID)
- created_at
- last_accessed  
- last_saved

**orchestrator_state** - Full orchestrator state
- user_id
- state_data (pickled orchestrator)
- framework_data (JSON)
- decisions_count
- patterns_count
- last_update

**decision_history** - Individual decisions
- user_id
- situation
- chosen_option
- rejected_options
- reasoning
- timestamp

**learning_patterns** - Identified patterns
- user_id
- pattern_type
- pattern_data
- confidence
- created_at

### How State is Managed

1. **First Visit**
   - System generates unique user_id
   - Stored in browser session cookie
   - Creates new orchestrator instance
   - Saves initial state to database

2. **Returning Visit**
   - Browser sends user_id in session
   - System loads orchestrator from database
   - All your learning restored!
   - Continues where you left off

3. **During Use**
   - Orchestrator kept in memory (fast!)
   - Auto-saved to database on every change
   - Best of both: speed + persistence

## FAQ

**Q: What if I lose my browser cookies?**

A: You'll get a new user_id and start fresh. Your old data is still in the database though - just needs the old user_id to access it.

**Q: Can I access my data from multiple devices?**

A: Currently each browser session gets a unique ID. To share across devices, you'd need to:
1. Export data from device 1
2. Import on device 2
(Or we could add user authentication!)

**Q: How much data can it store?**

A: SQLite can handle millions of records. You're fine! The database will grow over time but it's very efficient.

**Q: What if the server restarts?**

A: No problem! Your data is in the database file (orchestrator_data.db). When the server starts again, it loads from the database.

**Q: Is my data private?**

A: Yes! It's stored locally on the server you're running. Not sent anywhere else. Each user_id is unique and private.

**Q: Can I delete my data?**

A: Yes, though we don't have a UI button yet. The database can be cleared or specific users deleted using the persistence API.

## Benefits of Persistent Storage

### For Phone Users

✅ **Reliability**: Phone battery dies? Data safe!
✅ **Convenience**: Close browser, open later, everything there
✅ **Peace of Mind**: No anxiety about losing progress
✅ **Multi-tasking**: Switch apps freely, come back anytime

### For Learning

✅ **Long-term memory**: Builds understanding over weeks/months
✅ **Pattern recognition**: More decisions = better predictions
✅ **Historical context**: See how preferences evolved
✅ **Continuity**: Uninterrupted learning journey

### For Development

✅ **Debugging**: Can inspect database to understand behavior
✅ **Analytics**: Track learning progress over time
✅ **Recovery**: If something crashes, data is safe
✅ **Export/Import**: Backup and restore functionality

## Conclusion

**Your learning orchestrator has a persistent memory!**

Just like you remember things even after sleeping, the orchestrator remembers your preferences even after the browser closes. It's always ready to pick up where you left off.

**Safe, reliable, and automatic.** 🎉
