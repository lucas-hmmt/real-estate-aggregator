import React from 'react';

function Table({ children }) {
  return <table className="table">{children}</table>;
}

export function TableHead({ children }) {
  return <thead className="table-head">{children}</thead>;
}

export function TableBody({ children }) {
  return <tbody className="table-body">{children}</tbody>;
}

export function TableRow({ children }) {
  return <tr className="table-row">{children}</tr>;
}

export function TableHeaderCell({ children, ...props }) {
  return (
    <th className="table-header-cell" {...props}>
      {children}
    </th>
  );
}

export function TableCell({ children, ...props }) {
  return (
    <td className="table-cell" {...props}>
      {children}
    </td>
  );
}

export default Table;
