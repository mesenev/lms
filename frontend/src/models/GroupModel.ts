import type { UserModel } from "@/models/UserModel";

export interface GroupModel {
    id: number,
    course: number,
    group_schedule: JSON | null,
    points_for_passing: JSON | null,
    students: Array<number>,
    staff: Array<number>,
}