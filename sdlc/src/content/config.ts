import { defineCollection, z } from 'astro:content';

const commands = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    purpose: z.string(),
    input: z.string(),
    output: z.string(),
    path: z.enum(["conversation", "document", "both"]),
    sortOrder: z.number(),
  }),
});

export const collections = { commands };
