export default interface ProblemModel {
  id: number;
  lesson: number;
  type: string;
  name: string;
  description: string;
  completed: boolean;
  manual: boolean;
  cats_material_url: string;
  language: Array<string> | null; //Todo : fix this
}
