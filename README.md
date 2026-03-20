# Medium Blogs Repository

A chronologically organized collection of my Medium blog posts, code samples, and associated resources.

## Quick Links

- **[Browse Posts](./posts)** - All blog posts organized by year and month
- **[By Category](./categories)** - Browse posts by topic/category
- **[By Tags](./tags)** - Search posts by tags
- **[Template](./TEMPLATE.md)** - Use this template to create new posts

## Repository Structure

```
medium_blogs/
├── posts/                    # Main blog content (chronologically organized)
│   ├── 2024/                # Year folders
│   │   ├── 01-12/           # Month folders (01 = January, 12 = December)
│   │   │   ├── post-slug/   # Page bundle (folder with post + assets)
│   │   │   │   ├── index.md # Post content with front-matter
│   │   │   │   ├── code/    # Code samples (optional)
│   │   │   │   └── images/  # Article images (optional)
│   │   │   └── another-post.md  # Or standalone markdown files
│   ├── 2025/
│   ├── 2026/
│   └── archive/             # Older posts (3+ years old)
├── tags/                    # Tag index pages (auto-populated)
├── categories/              # Category index pages (auto-populated)
├── assets/                  # Shared images, diagrams, templates
├── TEMPLATE.md              # Template for creating new posts
├── LICENSE                  # Apache 2.0 License
└── README.md               # This file
```

## Adding a New Post

### Step 1: Create a Post Folder
Create a folder in the appropriate month using the naming convention `post-slug`:

```
posts/2026/03/my-new-post/
```

### Step 2: Create index.md
Create `index.md` inside the folder with your post content and front-matter:

```markdown
---
title: "My Article Title"
date: 2026-03-19
updated: 2026-03-19
categories: 
  - category-name
tags: 
  - tag1
  - tag2
  - tag3
medium_url: "https://medium.com/@yourhandle/article-url"
---

# My Article Title

Your content here...
```

### Step 3: Add Code & Images (Optional)
- Create `code/` folder for code samples
- Create `images/` folder for article images
- Reference them using relative paths: `./code/example.js`, `./images/diagram.png`

### Step 4: Reference the Template
See [TEMPLATE.md](./TEMPLATE.md) for a complete example with all available metadata fields.

## Front Matter Metadata

Essential fields for each post:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Article title |
| `date` | YYYY-MM-DD | Publication date |
| `updated` | YYYY-MM-DD | Last update date |
| `categories` | array | Primary content categories |
| `tags` | array | Search/discovery tags (3-5 recommended) |
| `medium_url` | string | Link to Medium article |
| `difficulty` | string | `beginner` \| `intermediate` \| `advanced` (optional) |
| `series` | string | Series name if multi-part (optional) |
| `series_part` | number | Part number in series (optional) |
| `related` | array | Paths to related posts (optional) |

## Discovery Options

Posts can be discovered through:

- **Chronologically:** Browse [posts/](./posts) → year → month
- **By Category:** Browse [categories/](./categories) for topic-based discovery
- **By Tags:** Browse [tags/](./tags) for tag-based discovery
- **Recent Posts:** Check the current month folders

## Guidelines

### Naming Conventions
- Folder/file names: Use lowercase with hyphens (`my-post-title`)
- Avoid spaces and special characters
- Keep names descriptive and URL-friendly

### Code Samples
- Place runnable code in `code/` subfolders within posts
- Include a `README.md` in code folders with setup/run instructions
- Use language-specific file extensions (`.js`, `.py`, `.java`, etc.)

### Images & Assets
- Store article images in `images/` subfolders
- Keep images under 1MB when possible
- Use descriptive filenames

### Post Organization
- One major post per folder (page bundle)
- Use consistent formatting and markdown style
- Link related posts using relative paths
- Update front-matter when posts are edited

## Statistics

- **License:** Apache 2.0
- **First Post:** See oldest post in archive
- **Total Posts:** Add up individual month counts

## Contributing

This is a personal blog repository. To propose changes:

1. Follow the structure and template guidelines
2. Ensure all front-matter metadata is complete
3. Test relative links before publishing
4. Keep code samples runnable and documented

## License

All content in this repository is licensed under the Apache License 2.0. See [LICENSE](./LICENSE) for details.

---

**Last Updated:** March 19, 2026  
**Total Posts:** See individual year/month folders for counts
