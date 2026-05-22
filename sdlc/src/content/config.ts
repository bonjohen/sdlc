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

const artifacts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    type: z.enum(["prompt", "generated"]),
    command: z.string().optional(),
    excerpt: z.boolean().default(false),
    sortOrder: z.number(),
  }),
});

const lessons = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    category: z.enum(["architecture", "process", "meta"]),
    sortOrder: z.number(),
  }),
});

export const collections = { commands, artifacts, lessons };
