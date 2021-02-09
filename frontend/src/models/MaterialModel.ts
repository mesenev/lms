import { TutorialModel } from '@/models/TutorialModel';

export default interface MaterialModel extends TutorialModel {
  lesson: number;
  content_type: string;
  content: string;
}
