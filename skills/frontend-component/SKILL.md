---
name: frontend-component
description: Use when the user requests a new UI component (React, Vue, Svelte, etc.). Scaffolds the component using the existing design system, includes tests, and adds Storybook (or equivalent) entry if the codebase uses it. Matches existing component conventions exactly — does NOT invent new patterns.
allowed_tools: Read, Edit, Write, Bash, Grep
---

# Frontend component

## When to use this skill

The user asks for a new UI component, screen, or visual element.

## Procedure

1. **Read 2-3 existing components in the same module.** Note: file structure, prop typing approach, styling system (Tailwind classes, CSS modules, styled-components, etc.), default-export vs named-export convention, test framework, story format.
2. **Read the design system documentation** if one exists: `docs/design-system.md`, Figma references, or the `components/ui/` directory's README. Match the design tokens (colors, spacing, typography).
3. **State the plan to the user.** Component name, props, variants (if any), files to create. Wait for approval.
4. **Implement:**
   - The component file
   - Type definitions (TypeScript interface, PropTypes, etc.)
   - Default values for optional props
   - Accessibility attributes (aria-*, roles, keyboard navigation)
   - Tests covering: render with required props, render with each variant, interaction (click/keyboard), accessibility (axe-core if available)
   - Storybook story (if the codebase uses Storybook): one story per variant
5. **Run `verify`.** Must pass.

## Output

The diff with the component, tests, and stories. Summary lists:
- Design-system tokens used
- Accessibility features (focus management, ARIA, keyboard support)
- Variants supported
- Conventions matched / deviations explained

## Forbidden

- Do not invent design tokens. Use the existing palette, spacing, type scale.
- Do not skip accessibility. Components without keyboard support and ARIA are not done.
- Do not use inline styles unless the existing codebase does. Match the styling system.
- Do not create a new directory structure. Match what's there.
- Do not skip tests. "It's just UI" is not an exception.

## References

- The codebase's `components/ui/` (or equivalent) for shape examples
- The design system docs (if absent, ASK whether to create them)
- WCAG 2.1 AA as the floor for accessibility
