export const allTools = ["run_coder_agent", "run_git_agent", "run_docs_agent"];

export async function copyToClipboard(text: string) {
  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    console.error('Failed to copy text: ', err);
  }
}
export function stringToColor(str: string): string {
  // Generate hash from string
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 2) - hash);
  }

  // Convert to HSL to ensure visually distinct colors
  const h = Math.abs(hash) % 360; // Hue: 0-360
  const s = 30 + (Math.abs(hash) % 30); // Saturation: 30-60%
  const l = 85 + (Math.abs(hash) % 10); // Lightness: 85-95%

  // Add secondary hue rotation for more variation
  const h2 = (h + 137) % 360; // Golden angle rotation
  const finalHue = hash % 2 === 0 ? h : h2;

  return `hsl(${finalHue}, ${s}%, ${l}%)`;
}