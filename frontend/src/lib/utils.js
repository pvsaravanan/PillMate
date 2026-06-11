import { clsx } from "clsx";
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export function deduplicateMedications(medsList) {
  const seen = new Set();
  const deduped = [];
  
  for (const med of medsList) {
    if (!med.name) continue;
    const normalizedKey = `${med.name.trim().toLowerCase()}-${(med.dosage || '').trim().toLowerCase()}`;
    if (!seen.has(normalizedKey)) {
      seen.add(normalizedKey);
      deduped.push(med);
    }
  }
  return deduped;
}
