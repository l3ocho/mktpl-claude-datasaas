# saas-api-platform Plugin - CLAUDE.md Integration

Add this section to your project's CLAUDE.md to enable saas-api-platform plugin features.

## Suggested CLAUDE.md Section

```markdown
## API Platform Integration

This project uses the saas-api-platform plugin for API development workflows.

### Configuration

Run `/api setup` to auto-detect framework and configure project paths.
Settings stored in `.api-platform.json` in project root.

### Available Commands

| Command | Purpose |
|---------|---------|
| `/api setup` | Detect framework and configure project |
| `/api scaffold <resource>` | Generate CRUD routes, models, schemas |
| `/api validate` | Check routes against OpenAPI spec |
| `/api docs` | Generate/update OpenAPI specification |
| `/api test-routes` | Generate endpoint test cases |
| `/api middleware <type>` | Add auth, CORS, rate-limit, logging |

### When to Use

- **Starting a new resource**: `/api scaffold orders` generates routes, models, and registers the router
- **Before PR/deploy**: `/api validate` ensures spec and code are in sync
- **After route changes**: `/api docs --update` refreshes the OpenAPI spec
- **Adding infrastructure**: `/api middleware auth` adds JWT authentication
- **Before release**: `/api test-routes --coverage=full` generates comprehensive tests

### Conventions

- All routes follow RESTful naming (plural nouns, no verbs in paths)
- Versioning via URL prefix (`/v1/`) when configured
- Pagination on all list endpoints (page, page_size parameters)
- Consistent error response format with error codes and request IDs
```

## Typical Workflows

### New Resource
```
/api scaffold products
/api docs --update
/api test-routes products
/api validate
```

### Add Authentication
```
/api middleware add auth
/api validate --strict
```

### Pre-Release Check
```
/api validate --strict
/api test-routes --coverage=full
```
