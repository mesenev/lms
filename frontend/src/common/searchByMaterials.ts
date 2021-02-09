import MaterialModel from '@/models/MaterialModel';

export default function searchByMaterials(
  query: string, arrayOfMaterials: MaterialModel[]
): MaterialModel[] {
  // if there is no query
  if (!query) {
    return arrayOfMaterials;
  }
  // if there is
  return arrayOfMaterials.filter((material) => {
    return material.name.toLowerCase().includes(query.toLowerCase())
  });
}
