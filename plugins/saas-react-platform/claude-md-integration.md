# saas-react-platform Plugin - CLAUDE.md Integration

Add this section to your project's CLAUDE.md to enable saas-react-platform plugin features.

## Suggested CLAUDE.md Section

```markdown
## React Development (saas-react-platform)

This project uses the saas-react-platform plugin for React frontend development.

### Configuration

**Framework**: Auto-detected from package.json and project structure
**TypeScript**: Auto-detected from tsconfig.json
**CSS Approach**: Auto-detected (Tailwind, CSS Modules, styled-components)

### Available Commands

| Command | Purpose |
|---------|---------|
| `/react setup` | Configure framework detection and conventions |
| `/react component` | Scaffold component with types and tests |
| `/react route` | Add route with page, layout, error boundary |
| `/react state` | Set up state management pattern |
| `/react hook` | Generate custom hook with types and tests |
| `/react lint` | Audit component tree for anti-patterns |

### Component Conventions

- Functional components only (no class components)
- TypeScript interfaces for all props
- Co-located tests (`Component.test.tsx` beside `Component.tsx`)
- Barrel files (`index.ts`) for clean imports

### State Management Guide

| Complexity | Pattern | Example |
|------------|---------|---------|
| Simple (theme, locale) | React Context | `/react state theme --pattern context` |
| Medium (cart, filters) | Zustand | `/react state cart --pattern zustand` |
| Complex (entities, async) | Redux Toolkit | `/react state products --pattern redux` |

### Typical Workflow

```
/react setup                                    # First-time detection
/react component DataTable --type ui            # Scaffold component
/react route dashboard --layout DashboardLayout # Add route
/react lint src/components/                     # Check for issues
```
```

## Environment Variables

No environment variables required. All configuration is auto-detected from the project structure.

## Typical Workflows

### New Feature Development
```
/react component FeatureName --type page        # Create page component
/react route feature-name --layout MainLayout   # Add route
/react state featureData --pattern zustand       # Set up state
/react hook useFeatureData --type data           # Create data hook
/react lint src/features/feature-name/          # Validate
```

### Component Library
```
/react component Button --type ui               # Presentational component
/react component Modal --type ui                # Another component
/react lint src/components/                     # Audit all components
```

### Form Development
```
/react component ContactForm --type form        # Form with validation
/react hook useContactForm --type form           # Form logic hook
/react lint src/components/ContactForm/         # Check form patterns
```
