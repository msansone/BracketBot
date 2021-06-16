
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BracketImageGeneratorTool
{
    class Program
    {
        static void Main(string[] args)
        {
            List<string> items = new List<string>();
            
            string name = args[0];

            int round = Convert.ToInt32(args[1]);

            int matchup = Convert.ToInt32(args[2]);

            List<List<string>> roundEntries = new List<List<string>>();

            for (int i = 3; i < args.Count<string>() - 1; i++)
            {
                string entriesForCurrentRound = args[i];

                List<string> entries = entriesForCurrentRound.Split('|').ToList();

                roundEntries.Add(entries);
            }

            string winner = args[args.Count<string>() - 1];

            generateImage(name, roundEntries, round, matchup, winner);
        }
        
        private static void createDirectoryIfNotExist(string path)
        {
            bool directoryExists = System.IO.Directory.Exists(path);

            if (directoryExists == false)
            {
                System.IO.Directory.CreateDirectory(path);
            }
        }

        private static int findNextPowerOf2(int n)
        {
            // decrement `n` (to handle the case when `n` itself is a power of 2)
            n = n - 1;

            // do till only one bit is left
            int val = n & (n - 1);

            while (val != 0)
            {
                // unset rightmost bit
                n = n & n - 1;

                val = n & (n - 1);
            }

            // `n` is now a power of two (less than `n`)

            // return next power of 2
            return n << 1;
        }

        private static void generateImage(string name, List<List<string>> roundEntries, int round, int matchup, string winner)
        {
            Bitmap bmpTemp = new Bitmap(10, 10);

            Graphics g = Graphics.FromImage(bmpTemp);

            try
            {
                int slots = findNextPowerOf2(roundEntries[0].Count / 2);
                
                if (slots > 0)
                {
                    // Get the number of rounds in the bracket.
                    int numberOfRounds = (int)Math.Log((double)slots, 2.0);
                    
                    float borderSize = 10.0f;

                    // Get the slot size.
                    Font f = new Font(FontFamily.GenericSansSerif, 12.0f);

                    Font titleFont = new Font(FontFamily.GenericSansSerif, 16.0f);
                    
                    float widestStringWidth = 0.0f;

                    float highestStringHeight = 0.0f;

                    foreach (string entry in roundEntries[0])
                    {
                        SizeF size = g.MeasureString(entry, f);

                        if (size.Width > widestStringWidth)
                        {
                            widestStringWidth = size.Width;
                        }

                        if (size.Height > highestStringHeight)
                        {
                            highestStringHeight = size.Height;
                        }
                    }

                    SizeF titleSize = g.MeasureString(name, titleFont);

                    SizeF slotSize = new SizeF(widestStringWidth, highestStringHeight);

                    // Determine the image size.
                    Size paddingSize = new Size(10, 20);

                    // Size the vote count font so that it fits between two entries.

                    float fontSize = f.Size;

                    Font voteCountFont = new Font(FontFamily.GenericSansSerif, fontSize);

                    SizeF voteCountFontSize = g.MeasureString("0", voteCountFont);

                    while (voteCountFontSize.Height > paddingSize.Height)
                    {
                        fontSize -= 1;

                        voteCountFont = new Font(FontFamily.GenericSansSerif, fontSize);

                        voteCountFontSize = g.MeasureString("0", voteCountFont);
                    }


                    float connectorWidth = 10.0f;

                    float roundWidth = slotSize.Width + connectorWidth;
                    

                    int bitmapWidth = 0;
                                        
                    int bracketWidth = (int)(((numberOfRounds * 2) * (slotSize.Width + paddingSize.Width)) + (borderSize * 2));

                    if (titleSize.Width > bracketWidth)
                    {
                        bitmapWidth = (int)Math.Ceiling(titleSize.Width);
                    }
                    else
                    {
                        bitmapWidth = bracketWidth;
                    }

                    int bitmapHeight = (int)(((slots / 2) * (slotSize.Height + paddingSize.Height)) + (borderSize) + titleSize.Height);

                    Bitmap bmpBracket = new Bitmap(bitmapWidth, bitmapHeight);

                    Graphics gBmp = Graphics.FromImage(bmpBracket);

                    try
                    {
                        gBmp.FillRectangle(new SolidBrush(Color.White), 0, 0, bitmapWidth, bitmapHeight);

                        gBmp.DrawString(name, titleFont, new SolidBrush(Color.Black), (bitmapWidth / 2) - (titleSize.Width / 2), 0);

                        // Draw the bracket.
                        Pen p = new Pen(Color.Black, 1.0f);

                        float roundXLeftSide = borderSize;

                        float roundXRightSide = bitmapWidth - slotSize.Width - borderSize;

                        float roundY = borderSize;

                        // Store the connector merge points from the previous round, and use them to position the slots in the next round.
                        List<PointF> connectorMergePointsLeftSide = new List<PointF>();
                        List<PointF> previousConnectorMergePointsLeftSide = new List<PointF>();

                        List<PointF> connectorMergePointsRightSide = new List<PointF>();
                        List<PointF> previousConnectorMergePointsRightSide = new List<PointF>();

                        for (int i = 0; i < numberOfRounds; i++)
                        {
                            int slotsForRound = slots / (int)(Math.Pow(2, i + 1));

                            roundY = borderSize + titleSize.Height;
                            
                            // Prepare the merge points for the left side
                            PointF previousConnectorEndPoint2LeftSide = new PointF(0, 0);

                            connectorMergePointsLeftSide.Clear();

                            // Copy the previous merge points into the current merge points and clear the list of previous.
                            foreach (PointF previousMergePoint in previousConnectorMergePointsLeftSide)
                            {
                                connectorMergePointsLeftSide.Add(previousMergePoint);
                            }

                            previousConnectorMergePointsLeftSide.Clear();


                            // Prepare the merge points for the right side.
                            PointF previousConnectorEndPoint2RightSide = new PointF(0, 0);

                            connectorMergePointsRightSide.Clear();

                            // Copy the previous merge points into the current merge points and clear the list of previous.
                            foreach (PointF previousMergePoint in previousConnectorMergePointsRightSide)
                            {
                                connectorMergePointsRightSide.Add(previousMergePoint);
                            }

                            previousConnectorMergePointsRightSide.Clear();
                            
                            for (int j = 0; j < slotsForRound; j++)
                            {
                                // Set the x to the x position of the previous merge points.
                                if (connectorMergePointsLeftSide.Count > 0)
                                {
                                    roundXLeftSide = connectorMergePointsLeftSide[j].X;

                                    roundXRightSide = connectorMergePointsRightSide[j].X - slotSize.Width;

                                    roundY = connectorMergePointsLeftSide[j].Y - (slotSize.Height / 2);
                                }

                                // Draw the left side slots.
                                if (i == round && (matchup == (int)Math.Floor((double)j/2)))
                                {
                                    gBmp.FillRectangle(new SolidBrush(Color.LightGoldenrodYellow), roundXLeftSide, roundY, slotSize.Width, slotSize.Height);
                                }

                                gBmp.DrawRectangle(p, roundXLeftSide, roundY, slotSize.Width, slotSize.Height);

                                // For the first round, draw the left side item name.

                                string entry = string.Empty;
                                int entryVoteCount = 0;

                                if (i < roundEntries.Count)
                                {
                                    if (j < roundEntries[i].Count)
                                    {
                                        entry = roundEntries[i][j * 2];

                                        Int32.TryParse(roundEntries[i][(j * 2) + 1], out entryVoteCount);
                                    }
                                }

                                SizeF stringSize = g.MeasureString(entry, f);

                                // Center the text.                                    
                                gBmp.DrawString(entry, f, new SolidBrush(Color.Black), (float)roundXLeftSide + (slotSize.Width / 2) - (stringSize.Width / 2), (float)roundY);

                                // Draw the vote count if it exists.
                                if (string.IsNullOrWhiteSpace(entry) == false)
                                {
                                    SizeF voteCountTextSize = g.MeasureString(entryVoteCount.ToString(), voteCountFont);

                                    gBmp.DrawString(entryVoteCount.ToString(), voteCountFont, new SolidBrush(Color.Blue), (float)roundXLeftSide, (float)roundY - voteCountTextSize.Height);
                                }


                                // Draw the left side connections.
                                PointF connectorEndPoint1LeftSide = new PointF(roundXLeftSide + slotSize.Width, roundY + (slotSize.Height / 2));

                                PointF connectorEndPoint2LeftSide;

                                if (i == numberOfRounds - 1)
                                {
                                    connectorEndPoint2LeftSide = new PointF(roundXLeftSide + slotSize.Width + connectorWidth, roundY + (slotSize.Height / 2));
                                }
                                else
                                {
                                    connectorEndPoint2LeftSide = new PointF(roundXLeftSide + slotSize.Width + (connectorWidth / 2), roundY + (slotSize.Height / 2));
                                }

                                gBmp.DrawLine(p, connectorEndPoint1LeftSide, connectorEndPoint2LeftSide);

                                if (j % 2 == 1)
                                {
                                    // Connect the connectors.
                                    gBmp.DrawLine(p, previousConnectorEndPoint2LeftSide, connectorEndPoint2LeftSide);

                                    PointF connectorMergePoint1 = new PointF(previousConnectorEndPoint2LeftSide.X, previousConnectorEndPoint2LeftSide.Y + ((connectorEndPoint2LeftSide.Y - previousConnectorEndPoint2LeftSide.Y) / 2));

                                    PointF connectorMergePoint2 = new PointF(previousConnectorEndPoint2LeftSide.X + (connectorWidth / 2), connectorMergePoint1.Y);
                                    
                                    gBmp.DrawLine(p, connectorMergePoint1, connectorMergePoint2);

                                    previousConnectorMergePointsLeftSide.Add(connectorMergePoint2);
                                }

                                // Save for the next step.
                                previousConnectorEndPoint2LeftSide = connectorEndPoint2LeftSide;

                                // Draw the right side of the bracket.

                                int slotIndex = j + slotsForRound;

                                if (i == round && (matchup == (int)Math.Floor((double)slotIndex / 2)))
                                {
                                    gBmp.FillRectangle(new SolidBrush(Color.LightGoldenrodYellow), roundXRightSide, roundY, slotSize.Width, slotSize.Height);
                                }

                                gBmp.DrawRectangle(p, roundXRightSide, roundY, slotSize.Width, slotSize.Height);

                                // For the first round, draw the right side item name.

                                entry = string.Empty;

                                if (i < roundEntries.Count)
                                {
                                    if (j + slotsForRound < roundEntries[i].Count)
                                    {
                                        entry = roundEntries[i][(j + slotsForRound) * 2];

                                        Int32.TryParse(roundEntries[i][((j + slotsForRound) * 2) + 1], out entryVoteCount);
                                    }
                                }

                                stringSize = g.MeasureString(entry, f);

                                // Center the text.                                    
                                gBmp.DrawString(entry, f, new SolidBrush(Color.Black), (float)roundXRightSide + (slotSize.Width / 2) - (stringSize.Width / 2), (float)roundY);

                                // Draw the vote count if it exists.
                                if (string.IsNullOrWhiteSpace(entry) == false)
                                {
                                    SizeF voteCountTextSize = g.MeasureString(entryVoteCount.ToString(), voteCountFont);

                                    gBmp.DrawString(entryVoteCount.ToString(), voteCountFont, new SolidBrush(Color.Blue), (float)roundXRightSide + slotSize.Width - voteCountTextSize.Width, (float)roundY - voteCountTextSize.Height);
                                }


                                // Draw the right side connections.
                                PointF connectorEndPoint1RightSide = new PointF(roundXRightSide, roundY + (slotSize.Height / 2));

                                PointF connectorEndPoint2RightSide = new PointF(roundXRightSide - (connectorWidth / 2), roundY + (slotSize.Height / 2));

                                if (i == numberOfRounds - 1)
                                {
                                    connectorEndPoint2RightSide = new PointF(roundXRightSide - connectorWidth, roundY + (slotSize.Height / 2));
                                }
                                else
                                {
                                    connectorEndPoint2RightSide = new PointF(roundXRightSide - (connectorWidth / 2), roundY + (slotSize.Height / 2));
                                }

                                gBmp.DrawLine(p, connectorEndPoint1RightSide, connectorEndPoint2RightSide);

                                if (j % 2 == 1)
                                {
                                    // Connect the connectors.
                                    gBmp.DrawLine(p, previousConnectorEndPoint2RightSide, connectorEndPoint2RightSide);

                                    PointF connectorMergePoint1 = new PointF(previousConnectorEndPoint2RightSide.X, previousConnectorEndPoint2RightSide.Y + ((connectorEndPoint2RightSide.Y - previousConnectorEndPoint2RightSide.Y) / 2));

                                    PointF connectorMergePoint2 = new PointF(previousConnectorEndPoint2RightSide.X - (connectorWidth / 2), connectorMergePoint1.Y);
                                    
                                    gBmp.DrawLine(p, connectorMergePoint1, connectorMergePoint2);

                                    previousConnectorMergePointsRightSide.Add(connectorMergePoint2);
                                }

                                // Save for the next step.
                                previousConnectorEndPoint2RightSide = connectorEndPoint2RightSide;

                                // If there are merge points from a previous iteration, there's no need to increase the Y position.
                                if (connectorMergePointsLeftSide.Count == 0)
                                {
                                    roundY += slotSize.Height + paddingSize.Height;
                                }
                            }
                        }

                        if (string.IsNullOrWhiteSpace(winner) == false)
                        {
                            string winnerLabel = "Winner: " + winner;

                            SizeF winnerLabelSize = gBmp.MeasureString(winnerLabel, titleFont);

                            gBmp.DrawString(winnerLabel, titleFont, new SolidBrush(Color.Black), (bitmapWidth / 2) - (winnerLabelSize.Width / 2), bitmapHeight - winnerLabelSize.Height);
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.Write(ex.Message);
                    }
                    finally
                    {
                        gBmp.Dispose();
                    }

                    createDirectoryIfNotExist("brackets");

                    bmpBracket.Save("brackets\\" + name.Replace(" ", "_") + ".png", ImageFormat.Png);
                }
            }
            catch (Exception ex)
            {
                Console.Write(ex.Message);
            }
            finally
            {
                bmpTemp.Dispose();

                g.Dispose();
            }
        }
    }
}