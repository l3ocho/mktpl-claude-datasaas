# Doc Guardian Integration

Add to your project's CLAUDE.md:

## Documentation Management

This project uses doc-guardian for automatic documentation synchronization.

### Behavior
- Documentation drift is detected automatically when files change
- Pending updates are queued silently during work
- Run `/doc-sync` to apply all pending documentation updates
- Run `/doc-audit` for a full project documentation review

### Documentation Files Tracked
- README.md (root and subdirectories)
- CLAUDE.md
- API documentation in docs/
- Docstrings in Python/TypeScript files

### Commit Convention
Documentation sync commits use: `docs: sync documentation with code changes`
