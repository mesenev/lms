import { TutorialModel } from '@/models/TutorialModel';

export default function <T extends TutorialModel>(query: string, arrayToSearch: T[]): T[] {
  if (!query) {
    return arrayToSearch;
  }
  return arrayToSearch.filter((element: T) => {
    return element.name.toLowerCase().includes(query.toLowerCase())
  });
}
