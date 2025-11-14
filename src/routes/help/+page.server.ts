// Server-side dummy data (SSR). Replace with DB/API later.
import type { PageServerLoad } from './$types';

const dummyVideos = Array.from({ length: 14 }).map((_, i) => {
  const id = `vid-${i+1}`;
  return {
    id,
    title: i === 0 ? "Getting Started — Product X" : `Feature Walkthrough #${i+1}`,
    description: "Step-by-step tutorial with tips & examples.",
    tags: (i % 3 === 0) ? ["getting-started","setup"] : (i % 3 === 1) ? ["advanced","workflow"] : ["admin","tips"],
    source: i % 2 === 0 ? `/assets/videos/sample-${(i%3)+1}.mp4` : `https://www.youtube.com/embed/dQw4w9WgXcQ`,
    type: i % 2 === 0 ? 'mp4' : 'youtube',
    duration: `${5 + (i % 10)}:${(i * 7) % 60}`.padStart(4, '0'),
    thumbnail: `/assets/thumbs/thumb-${(i%5)+1}.jpg`
  };
});

const dummyManuals = Array.from({ length: 9 }).map((_, i) => {
  const id = `man-${i+1}`;
  return {
    id,
    title: i === 0 ? "Quick Start Guide" : `User Manual — Section ${i+1}`,
    description: "Downloadable PDF with full instructions.",
    tags: i % 2 ? ["getting-started"] : ["admin"],
    file: `/assets/manuals/manual-${(i%3)+1}.pdf`,
    size: `${(1 + (i % 4))}.2MB`,
    preview: `/assets/manuals/preview-${(i%3)+1}.pdf`
  };
});

export const load: PageServerLoad = async () => {
  return {
    videos: dummyVideos,
    manuals: dummyManuals,
    allTags: Array.from(new Set([...dummyVideos.flatMap(v=>v.tags), ...dummyManuals.flatMap(m=>m.tags)]))
  };
};
