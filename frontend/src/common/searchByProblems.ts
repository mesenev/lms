import CatsProblemModel from '@/models/CatsProblemModel';
import ProblemModel from '@/models/ProblemModel';

export default function searchByProblems(
  query: string, arrayOfProblems: Array<ProblemModel | CatsProblemModel>,
): Array<ProblemModel | CatsProblemModel> {
  // if there is no query
  if (!query) {
    return arrayOfProblems;
  }
  // if there is
  return arrayOfProblems.filter((problem) => {
    return problem.name.toLowerCase().includes(query.toLowerCase())
  });
}
