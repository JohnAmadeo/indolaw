export interface TooltipData {
  contentKey: string;
  xPosition: number;
  yPosition: number;
}

export const emptyTooltip: TooltipData = {
  contentKey: '',
  xPosition: 0,
  yPosition: 0,
};
