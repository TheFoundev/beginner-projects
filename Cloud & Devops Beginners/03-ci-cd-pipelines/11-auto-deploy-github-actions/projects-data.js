// Projects data - demonstrates how CI/CD deploys changes
const PROJECTS = [
  {
    title: "Resume Website",
    description: "A responsive HTML resume with dark mode toggle, scroll animations, and localStorage-based theme preferences.",
    tech: ["HTML", "CSS", "JavaScript"],
    category: "frontend"
  },
  {
    title: "Docker Quote Generator",
    description: "A Python script packaged in a Docker container that generates random motivational quotes with 8-language support.",
    tech: ["Python", "Docker"],
    category: "backend"
  },
  {
    title: "CI/CD Test Pipeline",
    description: "A Python calculator with 10+ unit tests that automatically run on GitHub Actions every time code is pushed.",
    tech: ["Python", "Pytest", "GitHub Actions"],
    category: "devops"
  },
  {
    title: "Photo Gallery",
    description: "An image gallery with lazy loading, lightbox modal, and category filtering — deployed to AWS S3.",
    tech: ["HTML", "CSS", "JavaScript"],
    category: "frontend"
  },
  {
    title: "Serverless Contact Form",
    description: "A serverless form handler using AWS Lambda and SES, with no backend servers to manage.",
    tech: ["AWS Lambda", "Python", "Serverless"],
    category: "cloud"
  }
];
