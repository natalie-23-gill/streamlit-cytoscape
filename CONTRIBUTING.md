# Contributing to st-cytoscape

Thank you for your interest in contributing to st-cytoscape!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/natalie-23-gill/st-cytoscape.git
cd st-cytoscape
```

2. Install Python dependencies:
```bash
pip install -e .
pip install -r requirements-dev.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Start the frontend development server:
```bash
npm start
```

5. In another terminal, run the example app:
```bash
streamlit run examples/comprehensive_demo.py
```

## Making Changes

### Python Code

- Follow PEP 8 style guidelines
- Add type hints where appropriate
- Update docstrings for any API changes
- Run tests before submitting

### Frontend Code

- Use TypeScript for type safety
- Follow React best practices
- Test across different browsers

### Documentation

- Update README.md for new features
- Add examples for significant changes
- Document API changes

## Submitting Changes

1. Create a new branch for your feature/fix
2. Make your changes
3. Test thoroughly
4. Update documentation
5. Submit a pull request

## Issues Addressed

st-cytoscape was created to address specific issues from st-link-analysis:

- **PR #62**: Custom styling support
- **Issue #44**: Coordinate positioning
- **Issue #35**: Multi-tab resizing
- **Issue #63**: Customizable highlights

When contributing, please keep this focus on flexibility and customization.

## Code of Conduct

Be respectful and constructive in all interactions.

## Questions?

Open an issue for questions or discussions!
