export default interface User {
  id: number;
  name: string;
  courseLength: number;
  marks: Array<number>;
  attendance: Array<boolean>;
}
