// ========================================
// Fun Facts Data
// Organized by category for easy browsing
// ========================================

const FUN_FACTS = {
  science: [
    { text: "Octopuses have three hearts — two pump blood to their gills, one pumps it to the rest of the body.", source: "Marine Biology Journal" },
    { text: "Bananas are berries, but strawberries aren't — botanically speaking!", source: "Botanical Society of America" },
    { text: "A day on Venus is longer than a year on Venus.", source: "NASA Planetary Science" },
    { text: "Sharks have been around longer than trees.", source: "Paleontology Research" },
    { text: "There's a species of jellyfish that is biologically immortal.", source: "Nature Journal" }
  ],
  history: [
    { text: "The shortest war in history was between Britain and Zanzibar in 1896 — it lasted 38 to 45 minutes.", source: "Guinness World Records" },
    { text: "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid of Giza.", source: "History Today" },
    { text: "During WWII, the US military trained cats to carry microphones across enemy lines.", source: "Veterans History Project" },
    { text: "Ancient Egyptians used eye makeup to ward off the 'evil eye' and prevent infections.", source: "British Museum Archives" },
    { text: "The Great Wall of China is NOT visible from space with the naked eye.", source: "NASA Astronaut Testimony" }
  ],
  nature: [
    { text: "Honey never spoils — archaeologists found 3,000-year-old edible honey in Egyptian tombs.", source: "National Geographic" },
    { text: "A single cloud can weigh over 1 million pounds (about 500 tons).", source: "Smithsonian Institution" },
    { text: "Crows have the largest brain-to-body-mass ratio of any bird.", source: "University of Washington Study" },
    { text: "There are more trees on Earth than stars in the Milky Way — about 3 trillion trees.", source: "Yale University Research" },
    { text: "A group of flamingos is called a 'flamboyance'.", source: "Oxford English Dictionary" }
  ],
  tech: [
    { text: "The first computer bug was a real bug — a moth stuck in a relay in 1947.", source: "Harvard University Archives" },
    { text: "More Monopoly money is printed each year than real money in the world.", source: "Hasbro Archives" },
    { text: "The first 1GB hard drive (1980) weighed over 500 pounds and cost $40,000.", source: "IBM Historical Records" },
    { text: "The 'thumbs up' gesture originated from Roman gladiators.", source: "History Channel" },
    { text: "Wi-Fi was invented 9 years after the first web page was created.", source: "IEEE Wireless Archives" }
  ],
  food: [
    { text: "Pineapples take about 2 years to grow from a flower to a harvestable fruit.", source: "Hawaiian Pineapple Association" },
    { text: "The world's most expensive coffee is made from beans eaten by Asian palm civets.", source: "Guinness World Records" },
    { text: "Carrots were originally purple, not orange — orange carrots were bred in the 17th century.", source: "Dutch Agricultural Archives" },
    { text: "A single acre of wheat can produce enough flour to bake 3,000 loaves of bread.", source: "USDA Statistics" },
    { text: "The world's largest snow cone weighed over 15,000 pounds.", source: "Guinness World Records" }
  ]
};

function getAllFacts() {
  const all = [];
  for (const category in FUN_FACTS) {
    FUN_FACTS[category].forEach(fact => {
      all.push({ ...fact, category });
    });
  }
  return all;
}

const ALL_FACTS = getAllFacts();
