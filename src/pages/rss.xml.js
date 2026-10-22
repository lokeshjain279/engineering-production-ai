import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
export async function GET(context){const articles=await getCollection('articles');return rss({title:'Engineering Production AI',description:'ML inference, distributed systems, and MLOps engineering notes by Lokesh Jain.',site:context.site,items:articles.map(a=>({title:a.data.title,description:a.data.description,pubDate:a.data.pubDate,link:`/articles/${a.id}/`}))});}
