import matplotlib.pyplot as plt

# Bar positions and pixel coordinates digitized from the reference
bars = [
    (31,296,370),(46,319,379),(61,319,394),(76,348,355),
    (107,351,355),(153,350,356),(168,144,387),(183,334,359),
    (198,337,355),(214,343,361),(229,337,358),(244,345,357),
    (259,336,358),(275,346,355),(290,351,355),(305,346,355),
    (320,346,356),(336,348,357),(351,341,359),(366,348,355),
    (382,324,363),(397,309,427),(412,291,403),(427,304,410),
    (443,309,377),(458,341,356),(473,317,355),(488,326,362),
    (504,336,363),(519,351,355),(534,346,356),(565,338,359),
    (580,350,355),(595,348,356),(610,330,377),(626,342,355),
    (641,352,357),(656,345,355),(671,285,363),(687,338,355),
    (702,298,355),(717,341,357)
]

baseline = 355
scale = 20000 / 67

x = []
additions = []
deletions = []

for xpos, top, bottom in bars:
    x.append(xpos)
    additions.append(max(0, (baseline - top) * scale))
    deletions.append(-max(0, (bottom - baseline) * scale))

plt.figure(figsize=(9.16, 5.4))

plt.bar(x, additions, width=14, color='#30a147', label='Additions')
plt.bar(x, deletions, width=14, color='#df0c24', label='Deletions')

plt.xlim(20, 735)
plt.ylim(-42000, 80000)

plt.xticks(
    [113, 205, 297, 388, 480, 571, 663],
    ['Jul 2023', 'Jan 2024', 'Jul 2024', 'Jan 2025',
     'Jul 2025', 'Jan 2026', 'Jul 2026']
)

plt.yticks(
    [-40000, -20000, 0, 20000, 40000, 60000],
    ['-40k', '-20k', '0', '20k', '40k', '60k']
)

plt.ylabel('Frequency', rotation=270, labelpad=15)
plt.title('Code frequency', loc='left', fontweight='bold')

plt.grid(axis='both', linestyle='--', alpha=0.35)
plt.gca().yaxis.tick_right()
plt.gca().yaxis.set_label_position('right')

plt.legend(loc='center left', bbox_to_anchor=(1.08, 0.5), frameon=False)
plt.tight_layout()
plt.show()