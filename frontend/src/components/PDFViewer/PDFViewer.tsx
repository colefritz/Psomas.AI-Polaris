import { useEffect, useState } from 'react'
import { Document, Page, pdfjs } from 'react-pdf'
import { Citation } from '../../api'
import { Stack } from '@fluentui/react'
import styles from './PDFViewer.module.css'

// Set up the worker for react-pdf
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`

interface Props {
  citation: Citation
  onClose: () => void
}

export const PDFViewer = ({ citation, onClose }: Props) => {
  const [numPages, setNumPages] = useState<number | null>(null)
  const [pageNumber, setPageNumber] = useState<number>(citation.page_number || 1)
  const [scale, setScale] = useState(1.0)

  useEffect(() => {
    // Update page number when citation changes
    if (citation.page_number) {
      setPageNumber(citation.page_number)
    }
  }, [citation])

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages)
  }

  const renderHighlight = () => {
    if (!citation.highlight_coords) return null

    const { x, y, width, height } = citation.highlight_coords
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
    <Stack className={styles.container}>
      <Stack horizontal horizontalAlign="space-between" className={styles.header}>
        <div>
          {citation.filepath ? citation.filepath.split('/').pop() : 'Document'}
          {numPages && ` (Page ${pageNumber} of ${numPages})`}
        </div>
        <button onClick={onClose} className={styles.closeButton}>×</button>
      </Stack>
      
      <Stack horizontal horizontalAlign="center" className={styles.controls}>
        <button
          onClick={() => setPageNumber(prev => Math.max(1, prev - 1))}
          disabled={pageNumber <= 1}
        >
          Previous
        </button>
        <button
          onClick={() => setScale(prev => Math.max(0.5, prev - 0.1))}
        >
          Zoom Out
        </button>
        <button
          onClick={() => setScale(prev => Math.min(2, prev + 0.1))}
        >
          Zoom In
        </button>
        <button
          onClick={() => setPageNumber(prev => Math.min(numPages || prev, prev + 1))}
          disabled={numPages !== null && pageNumber >= numPages}
        >
          Next
        </button>
      </Stack>

      <div className={styles.documentContainer}>
        <Document
          file={citation.filepath || ''}
          onLoadSuccess={onDocumentLoadSuccess}
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
      </div>
    </Stack>
  )
}
