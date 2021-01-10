import LessonContent from '@/models/LessonContent';

export default function searchByMaterials(
  query: string, arrayOfMaterials: LessonContent[]
): LessonContent[] {
  // if there is no query
  if (!query) {
    return arrayOfMaterials;
  }
  // if there is
  return arrayOfMaterials.filter((material) => {
    return material.name.toLowerCase().includes(query.toLowerCase())
  });
}
