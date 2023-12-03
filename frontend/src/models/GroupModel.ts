import type { UserModel } from "@/models/UserModel";

export interface GroupModel {
    id: number,
    courseId: number,
    students: Array<UserModel>,
    teachers: Array<UserModel>,
}