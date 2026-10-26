// Photo data — in a real project these would be S3 object URLs
// Format: https://your-bucket.s3.region.amazonaws.com/photo-key.jpg
const PHOTOS = [
  {
    id: 1,
    src: "https://via.placeholder.com/600x400/4A90D9/ffffff?text=Mountain",
    thumb: "https://via.placeholder.com/300x200/4A90D9/ffffff?text=Mountain",
    title: "Mountain Peak at Dawn",
    description: "Early morning fog in the mountains",
    category: "nature",
    date: "2026-01-15",
    location: "Rocky Mountains",
    camera: "Sony A7R IV",
    focal: "24mm f/8",
    iso: "100"
  },
  {
    id: 2,
    src: "https://via.placeholder.com/400x600/764ba2/ffffff?text=City",
    thumb: "https://via.placeholder.com/300x200/764ba2/ffffff?text=City",
    title: "City Skyline",
    description: "Night view of the downtown skyline",
    category: "urban",
    date: "2026-01-10",
    location: "Downtown",
    camera: "Canon EOS R5",
    focal: "35mm f/2.8",
    iso: "400"
  },
  {
    id: 3,
    src: "https://via.placeholder.com/600x400/22c55e/ffffff?text=Forest",
    thumb: "https://via.placeholder.com/300x200/22c55e/ffffff?text=Forest",
    title: "Misty Forest",
    description: "A dense forest blanketed in morning mist",
    category: "nature",
    date: "2026-01-05",
    location: "National Park",
    camera: "Nikon Z7",
    focal: "50mm f/5.6",
    iso: "200"
  },
  {
    id: 4,
    src: "https://via.placeholder.com/500x400/ff6b6b/ffffff?text=Portrait",
    thumb: "https://via.placeholder.com/300x200/ff6b6b/ffffff?text=Portrait",
    title: "Portrait Session",
    description: "A candid portrait taken during golden hour",
    category: "people",
    date: "2026-01-03",
    location: "Beach",
    camera: "Sony A7III",
    focal: "85mm f/1.4",
    iso: "200"
  },
  {
    id: 5,
    src: "https://via.placeholder.com/600x300/fbbf24/ffffff?text=Sunset",
    thumb: "https://via.placeholder.com/300x200/fbbf24/ffffff?text=Sunset",
    title: "Coastal Sunset",
    description: "The sun dipping below the horizon over the ocean",
    category: "nature",
    date: "2026-01-01",
    location: "Santa Monica",
    camera: "Fuji X-T4",
    focal: "23mm f/11",
    iso: "100"
  },
  {
    id: 6,
    src: "https://via.placeholder.com/400x500/a855f7/ffffff?text=Market",
    thumb: "https://via.placeholder.com/300x200/a855f7/ffffff?text=Market",
    title: "Weekend Market",
    description: "Bustling stalls at the weekend farmers market",
    category: "people",
    date: "2026-01-08",
    location: "Downtown",
    camera: "Sony A6000",
    focal: "35mm f/4",
    iso: "800"
  },
  {
    id: 7,
    src: "https://via.placeholder.com/600x350/ec4899/ffffff?text=Architecture",
    thumb: "https://via.placeholder.com/300x200/ec4899/ffffff?text=Architecture",
    title: "Modern Architecture",
    description: "Geometric lines and clean forms of a modern building",
    category: "urban",
    date: "2025-12-28",
    location: "City Center",
    camera: "Canon EOS R6",
    focal: "24mm f/11",
    iso: "100"
  },
  {
    id: 8,
    src: "https://via.placeholder.com/550x400/f59e0b/ffffff?text=Lake",
    thumb: "https://via.placeholder.com/300x200/f59e0b/ffffff?text=Lake",
    title: "Mountain Lake",
    description: "A serene alpine lake reflecting the surrounding peaks",
    category: "nature",
    date: "2025-12-20",
    location: "Alpine Valley",
    camera: "Fuji X-T4",
    focal: "56mm f/2",
    iso: "200"
  }
];

const CATEGORIES = ["all", "nature", "urban", "people"];
