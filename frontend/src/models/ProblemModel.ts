export default interface ProblemModel {
  id: number;
  name: string;
  description: string;
  completed: boolean;
  manual: boolean;
  language: Array<string>;
}
