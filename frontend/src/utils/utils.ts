export const dateParse = function (date: string) {
  const answer = date.split('/', 3).map(value => Number(value));
  return new Date(answer[2], answer[1] - 1, answer[0]).getTime();
}
