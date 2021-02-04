export const statusAssociations: { [index: string]: string } = {
  'WA': '#f6d6d9',
  'OK': '#a7f0ba',
  'AW': '#d0ffc9',
  'TL': '#d0e2ff',
  'ML': '#e8daff',
  'NP': '#dde1e6',
  'CE': '#dfe2ff',
  'RJ': '#ffb8cf',
  'LI': '#c5ceff',
  'RE': '#fe9c9c',
  'PE': '#fec59c',
  'IL': '#ffe7b1',
  'WL': '#ffbfeb',
  'SV': '#8d8d8d',
  'IS': '#c8e8ea',
  'MR': '#f6d6d9',
  'BA': '#ff8c8c',
  'default': '#e0e0e0',
};

export const graphColor: { [index: string]: string } = {
  'successful': statusAssociations['OK'],
  'testing': statusAssociations['AW'],
  'wrong': statusAssociations['WA']
}
