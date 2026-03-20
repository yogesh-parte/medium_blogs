---
title: "Getting Started with Markdown for Blog Posts"
date: 2026-03-19
updated: 2026-03-19
categories: 
  - writing
  - tools
tags: 
  - markdown
  - blogging
  - documentation
medium_url: "https://medium.com/@yourhandle/getting-started-markdown"
difficulty: "beginner"
series: "Blogging Essentials"
series_part: 1
related: 
  - "2026/03/example-post-2"
---

# Getting Started with Markdown for Blog Posts

This is an example post demonstrating how to organize your Medium blogs in this repository.

## What is Markdown?

Markdown is a lightweight markup language that makes it easy to write formatted text without HTML. It's perfect for blog posts and is what Medium uses internally.

## Basic Formatting

### Headers
Use `#` symbols to create headers:

```markdown
# H1 Header
## H2 Header
### H3 Header
```

### Emphasis
- **Bold**: `**bold text**`
- *Italic*: `*italic text*`
- ~~Strikethrough~~: `~~strikethrough~~`

### Lists

Unordered lists:
- Item 1
- Item 2
- Item 3

Ordered lists:
1. First item
2. Second item
3. Third item

### Code Examples

Inline code: `console.log('hello')`

Code blocks with language specification:

```javascript
function greet(name) {
  console.log(`Hello, ${name}!`);
}
```

```python
def greet(name):
    print(f"Hello, {name}!")
```

## Working with Images

Store images in the `images/` folder and reference them:

```markdown
![Alt text](./images/your-image.png)
```

## Including Code Samples

Reference code files from the `code/` folder:

```markdown
See [example.js](./code/example.js) for a complete implementation.
```

## Links

- [Markdown Guide](https://www.markdownguide.org/)
- [Medium's Writing Guide](https://help.medium.com/)
- [CommonMark Spec](https://spec.commonmark.org/)

## Blockquotes

> "Markdown is a simple and elegant way to write formatted text on the web."
> — This repository

## Tables

| Feature | Markdown | HTML |
| --- | --- | --- |
| Simple | ✓ | ✗ |
| Readable | ✓ | ✗ |
| Powerful | ✓ | ✓ |

## Next Steps

1. Create a new folder in `posts/2026/03/your-post-slug/`
2. Copy the structure of this example post
3. Write your content in markdown
4. Add images to the `images/` folder
5. Add code samples to the `code/` folder
6. Update the front-matter metadata

## Resources

- [See the template](../../TEMPLATE.md) for complete metadata options
- [Browse other posts](../../) for more examples
- [Repository guidelines](../../README.md#guidelines)

---

**Published:** March 19, 2026  
**Last Updated:** March 19, 2026  
**Read on Medium:** [Link to Medium article](https://medium.com/@yourhandle/getting-started-markdown)
