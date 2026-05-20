export default function useTableFilter<T>(searchArray: any[], searchQuery: string, currentPage: number, pageRowsCount: number): { rows: T[], filtered: T[] } {
  if (!searchQuery) {
    return { rows: searchArray.slice((currentPage - 1) * pageRowsCount, (currentPage) * pageRowsCount), filtered: searchArray };
  }

  const filtered = searchArray.filter(
    (item) => Object.values(item).some(
      (value) => String(value).toLowerCase().includes(searchQuery.toLowerCase()),
    ),
  );

  return { rows: filtered.slice((currentPage - 1) * pageRowsCount, (currentPage) * pageRowsCount), filtered };
}
