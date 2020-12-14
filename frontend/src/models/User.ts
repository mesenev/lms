import PairModel from '@/models/UserProgress';

export default interface User {
  id: number;
  name: string;
  course: PairModel;
  group: string;
  mail: string;
  login: string;
}
