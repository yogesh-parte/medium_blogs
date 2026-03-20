// Example JavaScript code to demonstrate code organization
// Place this file in the code/ folder alongside your markdown post

function createMarkdownExample() {
  return {
    title: "Getting Started with Markdown",
    format: "markdown",
    tags: ["markdown", "blogging"],
    createLink: (text, url) => `[${text}](${url})`,
    createHeader: (level, text) => `${"#".repeat(level)} ${text}`,
    createCodeBlock: (language, code) => {
      return `\`\`\`${language}\n${code}\n\`\`\``;
    }
  };
}

// Export for use in other modules
module.exports = { createMarkdownExample };
