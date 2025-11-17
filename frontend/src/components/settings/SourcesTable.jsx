import React from 'react';
import Card from '../ui/Card';
import Table, { TableHead, TableBody, TableRow, TableHeaderCell, TableCell } from '../ui/Table';

function SourcesTable({ links }) {
  return (
    <Card className="settings-sources">
      <h2 className="section-title">Existing sources</h2>
      {links.length === 0 ? (
        <p className="text-secondary">
          No search links yet. Add one below.
        </p>
      ) : (
        <Table>
          <TableHead>
            <TableRow>
              <TableHeaderCell style={{ width: '70%' }}>URL</TableHeaderCell>
              <TableHeaderCell>Source</TableHeaderCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {links.map((link) => (
              <TableRow key={link.id}>
                <TableCell>
                  <a
                    href={link.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-link"
                  >
                    {link.link}
                  </a>
                </TableCell>
                <TableCell>{link.source}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </Card>
  );
}

export default SourcesTable;
