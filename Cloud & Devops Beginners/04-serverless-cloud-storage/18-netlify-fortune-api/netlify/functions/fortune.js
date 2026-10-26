/**
 * Netlify Serverless Function: Fortune Cookie API
 *
 * This function returns a random fortune as JSON.
 * Endpoint: /.netlify/functions/fortune
 *
 * Learn more: https://docs.netlify.com/functions/build-with-javascript/
 */

const fortunes = [
  "A new adventure is about to begin.",
  "Your curiosity will lead you to great discoveries.",
  "Small steps today lead to big achievements tomorrow.",
  "The best time to start was yesterday, the next best is now.",
  "Your creativity will surprise everyone around you.",
  "Expect something wonderful to happen today.",
  "Learning a new skill opens new doors.",
  "A friendly smile can change someone's day.",
  "Great things never came from comfort zones.",
  "Your potential is endless."
];

exports.handler = async (event, context) => {
  // Allow CORS for all origins
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
  };

  // Handle OPTIONS preflight request
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers,
      body: ""
    };
  }

  // Pick a random fortune
  const randomIndex = Math.floor(Math.random() * fortunes.length);

  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({
      fortune: fortunes[randomIndex],
      totalFortunes: fortunes.length
    })
  };
};
