export interface CatsProblemModel {
  id: number;
  name: string;
  code: string;
  contest_id: number;
  language: string;
  text_url: string;
  package_url: string;
  disabled: boolean;
  status: string;
  last_update_time: string;
  limits: {
    time: number;
    memory: number;
  };
  test_mode: string;
}
