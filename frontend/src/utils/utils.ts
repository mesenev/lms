export const dateParse = function (date: string) {
  debugger;
  const answer = date.split('/', 3).map(value => Number(value));
  return [answer[1], answer[0], answer[2]];
}

