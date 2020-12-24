import LessonModel from '@/models/LessonModel';

export default function searchByLessons(query: string,
                                        arrayOfLessons: LessonModel[]): LessonModel[] {
  // if there is no query
  if (!query) {
    return arrayOfLessons;
  }
  // if there is
  return arrayOfLessons.filter((lesson) => {
    return lesson.name.toLowerCase().includes(query.toLowerCase())
  });
}
