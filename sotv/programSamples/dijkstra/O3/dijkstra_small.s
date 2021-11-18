	.file	"dijkstra_small.c"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"Out of memory.\n"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB1:
.LHOTB1:
	.type	enqueue.part.0, @function
enqueue.part.0:
.LFB29:
	.cfi_startproc
	pushq	%rax
	.cfi_def_cfa_offset 16
	movq	stderr(%rip), %rcx
	movl	$.LC0, %edi
	movl	$15, %edx
	movl	$1, %esi
	call	fwrite
	movl	$1, %edi
	call	exit
	.cfi_endproc
.LFE29:
	.size	enqueue.part.0, .-enqueue.part.0
.LCOLDE1:
.LHOTE1:
	.section	.rodata.str1.1
.LC2:
	.string	" %d"
	.section	.text.unlikely
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4,,15
	.globl	print_path
	.type	print_path, @function
print_path:
.LFB23:
	.cfi_startproc
	movslq	%esi, %rax
	pushq	%r14
	.cfi_def_cfa_offset 16
	.cfi_offset 14, -16
	pushq	%r13
	.cfi_def_cfa_offset 24
	.cfi_offset 13, -24
	pushq	%r12
	.cfi_def_cfa_offset 32
	.cfi_offset 12, -32
	pushq	%rbp
	.cfi_def_cfa_offset 40
	.cfi_offset 6, -40
	movq	%rax, %rbp
	pushq	%rbx
	.cfi_def_cfa_offset 48
	.cfi_offset 3, -48
	movl	4(%rdi,%rax,8), %ebx
	cmpl	$9999, %ebx
	je	.L4
	movslq	%ebx, %rax
	movl	4(%rdi,%rax,8), %r12d
	cmpl	$9999, %r12d
	je	.L5
	movslq	%r12d, %rax
	movl	4(%rdi,%rax,8), %r13d
	cmpl	$9999, %r13d
	je	.L6
	movslq	%r13d, %rax
	movl	4(%rdi,%rax,8), %r14d
	cmpl	$9999, %r14d
	je	.L7
	movslq	%r14d, %rax
	movl	4(%rdi,%rax,8), %esi
	cmpl	$9999, %esi
	je	.L8
	call	print_path
.L8:
	movl	$1, %edi
	movl	%r14d, %edx
	movl	$.LC2, %esi
	xorl	%eax, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
.L7:
	movl	$1, %edi
	movl	%r13d, %edx
	movl	$.LC2, %esi
	xorl	%eax, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
.L6:
	movl	$1, %edi
	movl	%r12d, %edx
	movl	$.LC2, %esi
	xorl	%eax, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
.L5:
	movl	$1, %edi
	movl	%ebx, %edx
	movl	$.LC2, %esi
	xorl	%eax, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
.L4:
	movl	%ebp, %edx
	movl	$1, %edi
	movl	$.LC2, %esi
	xorl	%eax, %eax
	call	__printf_chk
	popq	%rbx
	.cfi_def_cfa_offset 40
	popq	%rbp
	.cfi_def_cfa_offset 32
	popq	%r12
	.cfi_def_cfa_offset 24
	popq	%r13
	.cfi_def_cfa_offset 16
	popq	%r14
	.cfi_def_cfa_offset 8
	movq	stdout(%rip), %rdi
	jmp	fflush
	.cfi_endproc
.LFE23:
	.size	print_path, .-print_path
	.section	.text.unlikely
.LCOLDE3:
	.text
.LHOTE3:
	.section	.text.unlikely
.LCOLDB4:
	.text
.LHOTB4:
	.p2align 4,,15
	.globl	enqueue
	.type	enqueue, @function
enqueue:
.LFB24:
	.cfi_startproc
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	movl	%edi, %r12d
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	movl	$24, %edi
	movl	%esi, %ebp
	movl	%edx, %ebx
	call	malloc
	testq	%rax, %rax
	movq	qHead(%rip), %rcx
	je	.L34
	testq	%rcx, %rcx
	movl	%r12d, (%rax)
	movl	%ebp, 4(%rax)
	movl	%ebx, 8(%rax)
	movq	$0, 16(%rax)
	jne	.L32
	jmp	.L35
	.p2align 4,,10
	.p2align 3
.L31:
	movq	%rdx, %rcx
.L32:
	movq	16(%rcx), %rdx
	testq	%rdx, %rdx
	jne	.L31
	movq	%rax, 16(%rcx)
	addl	$1, g_qCount(%rip)
	popq	%rbx
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L35:
	.cfi_restore_state
	popq	%rbx
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	movq	%rax, qHead(%rip)
	addl	$1, g_qCount(%rip)
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
.L34:
	.cfi_restore_state
	call	enqueue.part.0
	.cfi_endproc
.LFE24:
	.size	enqueue, .-enqueue
	.section	.text.unlikely
.LCOLDE4:
	.text
.LHOTE4:
	.section	.text.unlikely
.LCOLDB5:
	.text
.LHOTB5:
	.p2align 4,,15
	.globl	dequeue
	.type	dequeue, @function
dequeue:
.LFB25:
	.cfi_startproc
	movq	qHead(%rip), %rax
	testq	%rax, %rax
	je	.L43
	subq	$8, %rsp
	.cfi_def_cfa_offset 16
	movl	(%rax), %ecx
	movl	%ecx, (%rdi)
	movl	4(%rax), %ecx
	movq	%rax, %rdi
	movl	%ecx, (%rsi)
	movl	8(%rax), %ecx
	movl	%ecx, (%rdx)
	movq	16(%rax), %rdx
	movq	%rdx, qHead(%rip)
	call	free
	subl	$1, g_qCount(%rip)
	addq	$8, %rsp
	.cfi_def_cfa_offset 8
.L43:
	rep ret
	.cfi_endproc
.LFE25:
	.size	dequeue, .-dequeue
	.section	.text.unlikely
.LCOLDE5:
	.text
.LHOTE5:
	.section	.text.unlikely
.LCOLDB6:
	.text
.LHOTB6:
	.p2align 4,,15
	.globl	qcount
	.type	qcount, @function
qcount:
.LFB26:
	.cfi_startproc
	movl	g_qCount(%rip), %eax
	ret
	.cfi_endproc
.LFE26:
	.size	qcount, .-qcount
	.section	.text.unlikely
.LCOLDE6:
	.text
.LHOTE6:
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC8:
	.string	"Shortest path is 0 in cost. Just stay where you are."
	.section	.rodata.str1.1
.LC9:
	.string	"Shortest path is %d in cost. "
.LC10:
	.string	"Path is: "
	.section	.text.unlikely
.LCOLDB11:
	.text
.LHOTB11:
	.p2align 4,,15
	.globl	dijkstra
	.type	dijkstra, @function
dijkstra:
.LFB27:
	.cfi_startproc
	movdqa	.LC7(%rip), %xmm0
	movl	$rgnNodes, %eax
	.p2align 4,,10
	.p2align 3
.L46:
	addq	$16, %rax
	movaps	%xmm0, -16(%rax)
	cmpq	$rgnNodes+800, %rax
	jne	.L46
	cmpl	%esi, %edi
	movl	$100, ch(%rip)
	je	.L102
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	movslq	%edi, %rax
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	movl	$24, %edi
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	movl	%esi, %r12d
	movq	%rax, %rbx
	subq	$8, %rsp
	.cfi_def_cfa_offset 64
	movl	$0, rgnNodes(,%rax,8)
	movl	$9999, rgnNodes+4(,%rax,8)
	call	malloc
	testq	%rax, %rax
	movq	qHead(%rip), %rcx
	je	.L57
	testq	%rcx, %rcx
	movl	%ebx, (%rax)
	movl	$0, 4(%rax)
	movl	$9999, 8(%rax)
	movq	$0, 16(%rax)
	jne	.L90
	jmp	.L103
	.p2align 4,,10
	.p2align 3
.L70:
	movq	%rdx, %rcx
.L90:
	movq	16(%rcx), %rdx
	testq	%rdx, %rdx
	jne	.L70
	movq	%rax, 16(%rcx)
.L50:
	movl	g_qCount(%rip), %eax
	addl	$1, %eax
	testl	%eax, %eax
	movl	%eax, g_qCount(%rip)
	jle	.L104
	.p2align 4,,10
	.p2align 3
.L62:
	movq	qHead(%rip), %rdi
	testq	%rdi, %rdi
	je	.L101
	movl	(%rdi), %eax
	movl	%eax, iNode(%rip)
	movl	4(%rdi), %eax
	movl	%eax, iDist(%rip)
	movl	8(%rdi), %eax
	movl	%eax, iPrev(%rip)
	movq	16(%rdi), %rax
	movq	%rax, qHead(%rip)
	call	free
	subl	$1, g_qCount(%rip)
.L101:
	movslq	iNode(%rip), %rax
	movl	$0, i(%rip)
	movl	$rgnNodes, %r13d
	xorl	%ebp, %ebp
	movq	%rax, %r15
	leaq	(%rax,%rax,4), %rax
	leaq	(%rax,%rax,4), %r14
	salq	$4, %r14
	addq	$AdjMatrix, %r14
	.p2align 4,,10
	.p2align 3
.L61:
	movl	(%r14), %eax
	cmpl	$9999, %eax
	movl	%eax, iCost(%rip)
	je	.L54
	addl	iDist(%rip), %eax
	movl	0(%r13), %edx
	cmpl	$9999, %edx
	movl	%eax, %ebx
	je	.L56
	cmpl	%eax, %edx
	jle	.L54
.L56:
	movl	%ebx, 0(%r13)
	movl	%r15d, 4(%r13)
	movl	$24, %edi
	call	malloc
	testq	%rax, %rax
	movq	qHead(%rip), %rcx
	je	.L57
	testq	%rcx, %rcx
	movl	%ebp, (%rax)
	movl	%ebx, 4(%rax)
	movl	%r15d, 8(%rax)
	movq	$0, 16(%rax)
	jne	.L91
	jmp	.L105
	.p2align 4,,10
	.p2align 3
.L71:
	movq	%rdx, %rcx
.L91:
	movq	16(%rcx), %rdx
	testq	%rdx, %rdx
	jne	.L71
	movq	%rax, 16(%rcx)
.L59:
	addl	$1, g_qCount(%rip)
.L54:
	addl	$1, %ebp
	addq	$4, %r14
	addq	$8, %r13
	cmpl	$100, %ebp
	movl	%ebp, i(%rip)
	jne	.L61
	movl	g_qCount(%rip), %eax
	testl	%eax, %eax
	jg	.L62
.L104:
	movslq	%r12d, %rbx
	movl	$.LC9, %esi
	movl	$1, %edi
	movl	rgnNodes(,%rbx,8), %edx
	xorl	%eax, %eax
	call	__printf_chk
	xorl	%eax, %eax
	movl	$.LC10, %esi
	movl	$1, %edi
	call	__printf_chk
	movl	rgnNodes+4(,%rbx,8), %ebx
	cmpl	$9999, %ebx
	je	.L63
	movslq	%ebx, %rax
	movl	rgnNodes+4(,%rax,8), %ebp
	cmpl	$9999, %ebp
	je	.L64
	movslq	%ebp, %rax
	movl	rgnNodes+4(,%rax,8), %r13d
	cmpl	$9999, %r13d
	je	.L65
	movslq	%r13d, %rax
	movl	rgnNodes+4(,%rax,8), %r14d
	cmpl	$9999, %r14d
	je	.L66
	movslq	%r14d, %rax
	movl	rgnNodes+4(,%rax,8), %r15d
	cmpl	$9999, %r15d
	je	.L67
	movslq	%r15d, %rax
	movl	rgnNodes+4(,%rax,8), %esi
	cmpl	$9999, %esi
	je	.L68
	movl	$rgnNodes, %edi
	call	print_path
.L68:
	movl	$1, %edi
	movl	%r15d, %edx
	movl	$.LC2, %esi
	xorl	%eax, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
.L67:
	movl	$1, %edi
	movl	%r14d, %edx
	movl	$.LC2, %esi
	xorl	%eax, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
.L66:
	movl	$1, %edi
	movl	%r13d, %edx
	movl	$.LC2, %esi
	xorl	%eax, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
.L65:
	movl	$1, %edi
	movl	%ebp, %edx
	movl	$.LC2, %esi
	xorl	%eax, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
.L64:
	movl	$1, %edi
	movl	%ebx, %edx
	movl	$.LC2, %esi
	xorl	%eax, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
.L63:
	movl	%r12d, %edx
	movl	$.LC2, %esi
	movl	$1, %edi
	xorl	%eax, %eax
	call	__printf_chk
	movq	stdout(%rip), %rdi
	call	fflush
	addq	$8, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	movl	$10, %edi
	popq	%rbx
	.cfi_restore 3
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_restore 6
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_restore 12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_restore 13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_restore 14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_restore 15
	.cfi_def_cfa_offset 8
	jmp	putchar
	.p2align 4,,10
	.p2align 3
.L105:
	.cfi_restore_state
	movq	%rax, qHead(%rip)
	jmp	.L59
.L102:
	.cfi_def_cfa_offset 8
	.cfi_restore 3
	.cfi_restore 6
	.cfi_restore 12
	.cfi_restore 13
	.cfi_restore 14
	.cfi_restore 15
	movl	$.LC8, %edi
	jmp	puts
.L103:
	.cfi_def_cfa_offset 64
	.cfi_offset 3, -56
	.cfi_offset 6, -48
	.cfi_offset 12, -40
	.cfi_offset 13, -32
	.cfi_offset 14, -24
	.cfi_offset 15, -16
	movq	%rax, qHead(%rip)
	jmp	.L50
.L57:
	call	enqueue.part.0
	.cfi_endproc
.LFE27:
	.size	dijkstra, .-dijkstra
	.section	.text.unlikely
.LCOLDE11:
	.text
.LHOTE11:
	.section	.rodata.str1.1
.LC12:
	.string	"r"
.LC13:
	.string	"input.dat"
.LC14:
	.string	"%d"
	.section	.text.unlikely
.LCOLDB15:
	.section	.text.startup,"ax",@progbits
.LHOTB15:
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB28:
	.cfi_startproc
	pushq	%r13
	.cfi_def_cfa_offset 16
	.cfi_offset 13, -16
	pushq	%r12
	.cfi_def_cfa_offset 24
	.cfi_offset 12, -24
	movl	$.LC12, %esi
	pushq	%rbp
	.cfi_def_cfa_offset 32
	.cfi_offset 6, -32
	pushq	%rbx
	.cfi_def_cfa_offset 40
	.cfi_offset 3, -40
	movl	$.LC13, %edi
	movl	$AdjMatrix, %ebx
	movl	$AdjMatrix+40000, %r13d
	subq	$24, %rsp
	.cfi_def_cfa_offset 64
	movq	%fs:40, %rax
	movq	%rax, 8(%rsp)
	xorl	%eax, %eax
	call	fopen
	movq	%rax, %r12
	.p2align 4,,10
	.p2align 3
.L107:
	leaq	400(%rbx), %rbp
	.p2align 4,,10
	.p2align 3
.L108:
	leaq	4(%rsp), %rdx
	xorl	%eax, %eax
	movl	$.LC14, %esi
	movq	%r12, %rdi
	addq	$4, %rbx
	call	__isoc99_fscanf
	movl	4(%rsp), %eax
	movl	%eax, -4(%rbx)
	cmpq	%rbp, %rbx
	jne	.L108
	cmpq	%rbx, %r13
	jne	.L107
	movl	$50, %ecx
	xorl	%ebp, %ebp
	movl	$1374389535, %r12d
.L110:
	movl	%ecx, %eax
	movl	%ebp, %edi
	addl	$1, %ebp
	imull	%r12d
	movl	%ecx, %eax
	sarl	$31, %eax
	sarl	$5, %edx
	subl	%eax, %edx
	imull	$100, %edx, %ebx
	subl	%ebx, %ecx
	movl	%ecx, %esi
	movl	%ecx, %ebx
	call	dijkstra
	cmpl	$20, %ebp
	leal	1(%rbx), %ecx
	jne	.L110
	xorl	%edi, %edi
	call	exit
	.cfi_endproc
.LFE28:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE15:
	.section	.text.startup
.LHOTE15:
	.comm	iDist,4,4
	.comm	iCost,4,4
	.comm	i,4,4
	.comm	iNode,4,4
	.comm	iPrev,4,4
	.comm	ch,4,4
	.comm	rgnNodes,800,32
	.globl	g_qCount
	.bss
	.align 4
	.type	g_qCount, @object
	.size	g_qCount, 4
g_qCount:
	.zero	4
	.comm	AdjMatrix,40000,32
	.globl	qHead
	.align 8
	.type	qHead, @object
	.size	qHead, 8
qHead:
	.zero	8
	.section	.rodata.cst16,"aM",@progbits,16
	.align 16
.LC7:
	.long	9999
	.long	9999
	.long	9999
	.long	9999
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
