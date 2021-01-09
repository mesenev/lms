export default interface ProblemModel {
  id: number;
  type: string;
  name: string;
  description: string;
  completed: boolean;
  manual: boolean;
  language: Array<string>;
}
