import { useEffect, useState } from 'react'
import { Citation } from '../../api'
import { Stack } from '@fluentui/react'
import styles from './PDFViewer.module.css'
import { PDFRenderer } from './PDFRenderer'

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
        <PDFRenderer
          filepath={citation.filepath || ''}
          pageNumber={pageNumber}
          scale={scale}
          onLoadSuccess={onDocumentLoadSuccess}
          highlightCoords={citation.highlight_coords}
        />
      </div>
    </Stack>
  )
}
