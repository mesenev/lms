import type { BaseModel } from '@/models/BaseModel';

export default function <T extends BaseModel>(query: string, arrayToSearch: T[]): T[] {
    if (!query) {
        return arrayToSearch;
    }
    return arrayToSearch.filter((element: T) => {
        return element.name.toLowerCase().includes(query.toLowerCase());
    });
}
