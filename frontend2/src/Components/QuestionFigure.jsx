// Draws a question's figure: a graph or table described as data (question.figure),
// or the older uploaded picture (question.image_url) when there's no figure.
//
// Graph figure, coordinates in the graph's own units (0..x.max, 0..y.max):
// {
//   "type": "graph",
//   "alt": "What the graph shows, for screen readers",
//   "x": {"label": "Quantity", "max": 10},  "y": {"label": "Price", "max": 10},
//   "curves": [{"label": "Demand", "points": [[0, 9], [8.5, 0.5]], "color": "demand"}],
//   "guides": [[[0, 7], [6, 7]]],                 // dashed lines, each a list of points
//   "xTicks": [[2, "Q1"]],  "yTicks": [[7, "P4"]],
//   "points": [{"at": [2, 7], "label": "A", "pos": "ne"}],    // pos: n ne e se s sw w nw
//   "areas": [{"points": [[0, 9], [2, 7], [0, 7]], "color": "demand", "label": "CS"}],
//   "origin": "0"
// }
// Table figure:
// {"type": "table", "caption": "...", "columns": ["Price", "Qd"], "rows": [["$5", 10], ["$4", 12]]}

const COLORS = {
    demand: '#D62F2F', supply: '#1F5FD1', black: '#1A1A1A', green: '#1E8E3E',
    purple: '#7B3FC4', orange: '#E07400', gray: '#6B7280',
}
const color = (c) => COLORS[c] || c || COLORS.black

// Width, height and margins of the drawing (SVG units; it scales to fit its box)
const W = 480, H = 440, LEFT = 56, RIGHT = 84, TOP = 34, BOTTOM = 52
const PW = W - LEFT - RIGHT, PH = H - TOP - BOTTOM

const OFFSETS = {   // where a point's label sits relative to the point: [dx, dy, text-anchor]
    n: [0, -9, 'middle'], ne: [7, -8, 'start'], e: [9, 5, 'start'], se: [7, 17, 'start'],
    s: [0, 20, 'middle'], sw: [-7, 17, 'end'], w: [-9, 5, 'end'], nw: [-7, -8, 'end'],
}

const EconGraph = ({ fig }) => {
    const xMax = fig.x?.max ?? 10, yMax = fig.y?.max ?? 10
    const sx = (x) => LEFT + (x / xMax) * PW
    const sy = (y) => TOP + PH - (y / yMax) * PH
    const path = (pts) => pts.map(([x, y], i) => `${i ? 'L' : 'M'}${sx(x)},${sy(y)}`).join(' ')
    const baseY = TOP + PH

    return (
        <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={fig.alt || 'Graph'} className="w-full h-auto block"
            fontFamily="inherit" fontSize="16" fill="#1A1A1A">
            <title>{fig.alt || 'Graph'}</title>

            {(fig.areas || []).map((a, i) => (
                <polygon key={`a${i}`} points={a.points.map(([x, y]) => `${sx(x)},${sy(y)}`).join(' ')}
                    fill={color(a.color)} fillOpacity="0.18" stroke="none" />
            ))}

            {(fig.guides || []).map((g, i) => (
                <path key={`g${i}`} d={path(g)} fill="none" stroke="#1A1A1A" strokeWidth="1.2" strokeDasharray="6 5" />
            ))}

            {/* axes */}
            <path d={`M${LEFT},${TOP - 6} V${baseY} H${LEFT + PW + 8}`} fill="none" stroke="#1A1A1A" strokeWidth="1.6" />
            <text x={LEFT - 8} y={TOP - 14} textAnchor="start" fontSize="17">{fig.y?.label}</text>
            <text x={LEFT + PW + 8} y={baseY + 42} textAnchor="end" fontSize="17">{fig.x?.label}</text>
            {fig.origin != null && <text x={LEFT - 10} y={baseY + 22} textAnchor="end">{fig.origin}</text>}

            {(fig.xTicks || []).map(([x, label], i) => (
                <text key={`xt${i}`} x={sx(x)} y={baseY + 22} textAnchor="middle">{label}</text>
            ))}
            {(fig.yTicks || []).map(([y, label], i) => (
                <text key={`yt${i}`} x={LEFT - 10} y={sy(y) + 5} textAnchor="end">{label}</text>
            ))}

            {(fig.curves || []).map((c, i) => {
                const [lx, ly] = c.labelAt || c.points[c.points.length - 1]
                return (
                    <g key={`c${i}`}>
                        <path d={path(c.points)} fill="none" stroke={color(c.color)} strokeWidth="2.6" strokeLinejoin="round" />
                        {c.label && <text x={sx(lx) + (c.labelAt ? 0 : 8)} y={sy(ly) + 5} textAnchor="start"
                            fill={color(c.color)} fontWeight="600">{c.label}</text>}
                    </g>
                )
            })}

            {(fig.areas || []).filter((a) => a.label).map((a, i) => {
                const cx = a.points.reduce((s, p) => s + p[0], 0) / a.points.length
                const cy = a.points.reduce((s, p) => s + p[1], 0) / a.points.length
                const [lx, ly] = a.labelAt || [cx, cy]
                return <text key={`al${i}`} x={sx(lx)} y={sy(ly) + 5} textAnchor="middle" fontWeight="600">{a.label}</text>
            })}

            {(fig.points || []).map((p, i) => {
                const [dx, dy, anchor] = OFFSETS[p.pos || 'ne'] || OFFSETS.ne
                return (
                    <g key={`p${i}`}>
                        {p.dot && <circle cx={sx(p.at[0])} cy={sy(p.at[1])} r="3.5" />}
                        <text x={sx(p.at[0]) + dx} y={sy(p.at[1]) + dy} textAnchor={anchor} fontWeight="600">{p.label}</text>
                    </g>
                )
            })}
        </svg>
    )
}

const DataTable = ({ fig }) => (
    <table className="w-full text-center text-[#1A1A1A] border-collapse">
        {fig.caption && <caption className="pb-2 font-semibold">{fig.caption}</caption>}
        <thead>
            <tr>{fig.columns.map((c, i) => <th key={i} scope="col" className="border-b-2 border-[#1A1A1A] px-3 py-1.5">{c}</th>)}</tr>
        </thead>
        <tbody>
            {fig.rows.map((row, r) => (
                <tr key={r} className="even:bg-black/5">
                    {row.map((cell, i) => <td key={i} className="border-b border-black/15 px-3 py-1.5">{cell}</td>)}
                </tr>
            ))}
        </tbody>
    </table>
)

export const QuestionFigure = ({ question, className = '' }) => {
    const fig = question?.figure
    if (fig?.type === 'graph' || fig?.type === 'table') {
        return (
            <figure className={`bg-white rounded-xl p-3 ${className}`}>
                {fig.type === 'graph' ? <EconGraph fig={fig} /> : <DataTable fig={fig} />}
            </figure>
        )
    }
    if (question?.image_url) {
        return <figure className={`bg-white rounded-xl p-3 ${className}`}><img src={question.image_url} alt="" className="w-full" /></figure>
    }
    return null
}

export default QuestionFigure
