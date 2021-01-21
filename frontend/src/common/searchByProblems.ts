
export default function searchByProblems(
  query: string, arrayOfProblems: Array<{ name: string }>,
): Array<{ name: string }> {
  // if there is no query
  if (!query) {
    return arrayOfProblems;
  }
  // if there is
  return arrayOfProblems.filter((problem) => {
    return problem.name.toLowerCase().includes(query.toLowerCase())
  });
}
