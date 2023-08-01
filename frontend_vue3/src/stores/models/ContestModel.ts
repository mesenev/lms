export default interface CatsContestModel {
  id: number;
  name: string;
  short_descr: string;
  problems_url: string;
  start_date: Date;
  finish_date: Date;
  start_time: string;
  finish_time: string;
  freeze_time: string;
  unfreeze_time: string;
  registration: string;
  is_official: boolean;
  scoring: string;

}

export interface ContestModel {
  name: string;
  label: string;
  value: string;
}


