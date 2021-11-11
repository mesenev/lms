import { BaseModel } from '@/models/BaseModel';
import SubmitModel from '@/models/SubmitModel';


export interface ProblemStatsModel {
  green: number;
  yellow: number;
  red: number;
}

export default interface ProblemModel extends BaseModel {
  lesson: number;
  type: string;
  description: string;
  completed: boolean;
  manual: boolean;
  cats_id: number;
  cats_material_url: string;
  language: Array<string> | null; //Todo : fix this
  students?: {};
  submits?: Array<SubmitModel>;
  last_submit?: SubmitModel;
  stats?: ProblemStatsModel;
  de_options: string;
}
