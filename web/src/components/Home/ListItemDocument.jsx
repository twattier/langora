import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Accordion from '@mui/material/Accordion'
import AccordionSummary from '@mui/material/AccordionSummary'
import AccordionDetails from '@mui/material/AccordionDetails'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'

import ListItemSource from '../atoms/ListItemSource'
import { DisplayLines } from '../../utils/display'

export default function ListItemDocument(props) {
  const { document } = props

  return (
    <Stack justifyContent="center">
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          // aria-controls="panel1-content"
          // id="panel1-header"
        >
          <Typography variant="body2" color="secondary" sx={{ mr: 2 }}>
            {(document.score_total * 100).toFixed(2)}%
          </Typography>
          <ListItemSource source={document.source} />
        </AccordionSummary>
        <AccordionDetails>
          <Box>
            <Typography variant="caption">
              [{document.doc_type} - Chunk : {document.doc_chunk}]
            </Typography>
            <Typography variant="body2">
              <DisplayLines text={document.doc_text} />
            </Typography>
          </Box>
        </AccordionDetails>
      </Accordion>
    </Stack>
  )
}
