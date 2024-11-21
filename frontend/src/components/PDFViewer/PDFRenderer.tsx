'use client'

import { Document, Page, pdfjs } from 'react-pdf'
import styles from './PDFViewer.module.css'

// Set up the worker for react-pdf
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`

interface Props {
  filepath: string
  pageNumber: number
  scale: number
  onLoadSuccess: ({ numPages }: { numPages: number }) => void
  highlightCoords?: {
    x: number
    y: number
    width: number
    height: number
  }
}

export const PDFRenderer = ({ filepath, pageNumber, scale, onLoadSuccess, highlightCoords }: Props) => {
  const renderHighlight = () => {
    if (!highlightCoords) return null

    const { x, y, width, height } = highlightCoords
    return (
      <div
        className={styles.highlight}
        style={{
          position: 'absolute',
          left: `${x * scale}px`,
          top: `${y * scale}px`,
          width: `${width * scale}px`,
          height: `${height * scale}px`
        }}
      />
    )
  }

  return (
    <Document
      file={filepath || ''}
      onLoadSuccess={onLoadSuccess}
      className={styles.document}
    >
      <Page
        pageNumber={pageNumber}
        scale={scale}
        className={styles.page}
        renderTextLayer={false}
        renderAnnotationLayer={false}
      />
      {renderHighlight()}
    </Document>
  )
}
