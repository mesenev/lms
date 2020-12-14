export default interface UserProgress {
  id: number;
  name: string;
  courseLength: number;
  marks: Array<number>;
  attendance: Array<boolean>;
}
