import {Dictionary} from "vue-router/types/router";

export default interface UserProgress {
  id: number;
  //name: string;
  //marks: Array<number>;
  //attendance: Array<boolean>;
  lesson: number;
  solved: Dictionary<string>;
  user: number;
}
