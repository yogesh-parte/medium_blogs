# Blog Posts

All Medium blog posts organized chronologically by year and month.

## Navigation

- **[2024](./2024)** - Posts from 2024
- **[2025](./2025)** - Posts from 2025
- **[2026](./2026)** - Posts from 2026
- **[Archive](./archive)** - Older posts (3+ years old)

## Post Structure

Each post is organized as a page bundle:

```
posts/2024/01/
├── post-title/
│   ├── index.md          # Main post content with front-matter
│   ├── code/             # Code samples (optional)
│   │   ├── example.js
│   │   └── sample.css
│   └── images/           # Article images (optional)
│       ├── diagram.png
│       └── screenshot.jpg
└── another-post.md       # Standalone posts can be single files
```

## Adding a New Post

1. Create a folder in the appropriate month: `posts/YYYY/MM/post-slug/`
2. Create `index.md` with front-matter (use [TEMPLATE.md](../../TEMPLATE.md) as reference)
3. Add code samples in `code/` subfolder
4. Add images in `images/` subfolder
5. Reference the Medium URL in the front-matter

## Front Matter Metadata

Each post should include:

- `title` - Article title
- `date` - Publication date (YYYY-MM-DD)
- `updated` - Last update date
- `categories` - Primary content category
- `tags` - Search/discovery tags (3-5 recommended)
- `medium_url` - Link to Medium article
- `difficulty` - beginner | intermediate | advanced (optional)
- `series` - If part of a series (optional)
- `related` - Links to related posts (optional)

## Discovery

Posts can be discovered by:

- **Year/Month:** Browse chronologically above
- **Category:** Check [categories/](../../categories)
- **Tags:** Check [tags/](../../tags)
- **Search:** Use repository search functionality

## Statistics

- **Total Posts:** View individual year folders for counts
- **Last Updated:** See individual post dates

## Maintenance

- Add new posts to the appropriate month folder
- Keep archive updated for posts 3+ years old
- Update metadata in front-matter regularly
- Maintain tag consistency across posts
